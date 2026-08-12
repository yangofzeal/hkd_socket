#!/usr/bin/env python3
"""
HKD Socket 1 GiB WAN benchmark.

Measures two real TCP paths against the same initial file and update schedule:

  1) BASELINE: Python stdlib socket.sendfile(), retransmitting every full version.
  2) HKD:      hkd_socket.HKDSocket + TrackedFile.write_at(), initial snapshot
               then exact tracked deltas.

The receiver speaks the same F/D/X framing used by the existing hkd_socket
benchmark. Run the receiver on the WEST host and the client on the EAST host.

IMPORTANT:
- "versions" includes the initial version.
- Default: 1 GiB state, 100 versions, 1 MiB changed per later version.
- With 100 versions and a mandatory first full snapshot, the payload-reduction
  ceiling versus full retransmission is < 100x. A 261x ratio is mathematically
  impossible for this exact 100-version workload because HKD must send the
  initial 1 GiB once.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import random
import shutil
import socket as std_socket
import struct
import sys
import tempfile
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if (ROOT / "dist" / "hkd_socket").is_dir():
    sys.path.insert(0, str(ROOT / "dist"))
elif (ROOT / "src" / "hkd_socket").is_dir():
    sys.path.insert(0, str(ROOT / "src"))

try:
    import hkd_socket as socket
except ImportError:
    socket = None

BUF = 4 << 20
F = b"F"
D = b"D"
X = b"X"
K = b"K"
U64 = struct.Struct("!Q")
DH = struct.Struct("!QQ")
RH = struct.Struct("!QI")


def human(n):
    x = float(n)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if x < 1024.0 or unit == "TiB":
            return "%.3f %s" % (x, unit)
        x /= 1024.0


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb", buffering=0) as f:
        while True:
            b = f.read(BUF)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def recv_exact(sock, n):
    out = bytearray(n)
    view = memoryview(out)
    pos = 0
    while pos < n:
        got = sock.recv_into(view[pos:])
        if not got:
            raise EOFError("socket closed")
        pos += got
    return bytes(out)


def receiver_one(conn, out_path, label):
    rx = 0
    frames = 0
    full_frames = 0
    delta_frames = 0
    started = time.perf_counter()
    try:
        with open(out_path, "w+b", buffering=0) as out:
            while True:
                typ = recv_exact(conn, 1)
                rx += 1
                if typ == X:
                    break
                if typ == F:
                    raw = recv_exact(conn, U64.size)
                    rx += len(raw)
                    logical_size = U64.unpack(raw)[0]
                    out.seek(0)
                    left = logical_size
                    while left:
                        b = recv_exact(conn, min(BUF, left))
                        rx += len(b)
                        out.write(b)
                        left -= len(b)
                    out.truncate(logical_size)
                    conn.sendall(K)
                    frames += 1
                    full_frames += 1
                elif typ == D:
                    raw = recv_exact(conn, DH.size)
                    rx += len(raw)
                    logical_size, nranges = DH.unpack(raw)
                    for _ in range(nranges):
                        raw = recv_exact(conn, RH.size)
                        rx += len(raw)
                        off, length = RH.unpack(raw)
                        b = recv_exact(conn, length)
                        rx += len(b)
                        out.seek(off)
                        out.write(b)
                    out.truncate(logical_size)
                    conn.sendall(K)
                    frames += 1
                    delta_frames += 1
                else:
                    raise RuntimeError("bad frame type %r" % (typ,))
        elapsed = time.perf_counter() - started
        digest = sha256_file(out_path)
        print("SERVER_RESULT label=%s rx_bytes=%d rx=%s elapsed_s=%.6f "
              "frames=%d full_frames=%d delta_frames=%d sha256=%s" %
              (label, rx, human(rx), elapsed, frames, full_frames,
               delta_frames, digest), flush=True)
        return rx, elapsed, digest
    finally:
        conn.close()


def server(args):
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    ls = std_socket.socket(std_socket.AF_INET, std_socket.SOCK_STREAM)
    ls.setsockopt(std_socket.SOL_SOCKET, std_socket.SO_REUSEADDR, 1)
    ls.bind((args.bind, args.port))
    ls.listen(8)
    print("HKD_SOCKET_WAN_SERVER", flush=True)
    print("bind=%s port=%d out_dir=%s runs=%d" %
          (args.bind, args.port, out_dir, args.runs), flush=True)
    labels = ["baseline", "hkd"] + ["run%d" % i for i in range(3, args.runs + 1)]
    try:
        for i in range(args.runs):
            conn, addr = ls.accept()
            label = labels[i] if i < len(labels) else "run%d" % (i + 1)
            print("ACCEPT run=%d label=%s peer=%s:%s" %
                  (i + 1, label, addr[0], addr[1]), flush=True)
            receiver_one(conn, out_dir / ("%02d_%s.bin" % (i + 1, label)), label)
    finally:
        ls.close()


def make_base(path, size, seed):
    """Create deterministic high-entropy-ish data without retaining it in RAM."""
    if path.exists() and path.stat().st_size == size:
        return
    rng = random.Random(seed)
    block = 1 << 20
    with open(path, "wb", buffering=0) as f:
        left = size
        while left:
            n = min(block, left)
            # Deterministic; avoids relying on a compressible all-zero sparse file.
            b = bytes(rng.getrandbits(8) for _ in range(n))
            f.write(b)
            left -= n


def make_updates(size, versions, changed_bytes, seed):
    """
    Exactly one contiguous changed range per later version.
    This makes "changed_bytes per iteration" unambiguous.
    """
    rng = random.Random(seed)
    updates = []
    maxoff = size - changed_bytes
    if maxoff < 0:
        raise ValueError("changed_bytes exceeds file size")
    for _ in range(1, versions):
        off = rng.randrange(maxoff + 1)
        # Generate deterministic new literal bytes.
        data = bytes(rng.getrandbits(8) for _ in range(changed_bytes))
        updates.append((off, data))
    return updates


def apply_write(path, off, data):
    fd = os.open(str(path), os.O_RDWR)
    try:
        if hasattr(os, "pwrite"):
            os.pwrite(fd, data, off)
        else:
            os.lseek(fd, off, os.SEEK_SET)
            os.write(fd, data)
    finally:
        os.close(fd)


def sendfile_exact(sock, f, size):
    sent_total = 0
    off = 0
    while off < size:
        n = sock.sendfile(f, offset=off, count=size - off)
        if n is None:
            n = f.tell() - off
        if not n:
            raise RuntimeError("socket.sendfile stalled")
        off += n
        sent_total += n
    return sent_total


def run_baseline(host, port, src, updates):
    size = src.stat().st_size
    s = std_socket.create_connection((host, port))
    s.setsockopt(std_socket.IPPROTO_TCP, std_socket.TCP_NODELAY, 1)
    tx = 0
    start = time.perf_counter()
    try:
        versions = len(updates) + 1
        for i in range(versions):
            if i:
                off, data = updates[i - 1]
                apply_write(src, off, data)
            hdr = F + U64.pack(size)
            s.sendall(hdr)
            tx += len(hdr)
            with open(src, "rb", buffering=0) as f:
                tx += sendfile_exact(s, f, size)
            if recv_exact(s, 1) != K:
                raise RuntimeError("missing baseline ACK")
        s.sendall(X)
        tx += 1
    finally:
        s.close()
    elapsed = time.perf_counter() - start
    return {
        "tx": tx,
        "elapsed": elapsed,
        "sha256": sha256_file(src),
    }


def run_hkd(host, port, src, updates):
    if socket is None:
        raise SystemExit(
            "ERROR: hkd_socket is not importable. Install/place the HKD Socket "
            "package beside test.py before running client/local mode."
        )

    raw = std_socket.create_connection((host, port))
    raw.setsockopt(std_socket.IPPROTO_TCP, std_socket.TCP_NODELAY, 1)
    hs = socket.HKDSocket(raw)
    tracked = socket.TrackedFile(str(src))
    start = time.perf_counter()
    try:
        hs.sendfile(tracked)
        for off, data in updates:
            tracked.write_at(off, data)
            hs.sendfile(tracked)
        hs.finish()
        stats = hs.stats()
    finally:
        hs.close()
    elapsed = time.perf_counter() - start
    return {
        "tx": int(stats.wire_bytes),
        "elapsed": elapsed,
        "active_bytes": int(stats.active_bytes),
        "active_ranges": int(stats.active_ranges),
        "sha256": sha256_file(src),
    }


def client(args):
    size = int(args.size_gib * (1 << 30))
    changed = int(args.changed_mib * (1 << 20))
    versions = args.versions
    if versions < 2:
        raise SystemExit("--versions must be >= 2")
    if changed <= 0 or changed > size:
        raise SystemExit("invalid --changed-mib")

    work = Path(args.work_dir).resolve()
    work.mkdir(parents=True, exist_ok=True)
    base = work / "base.bin"
    baseline_src = work / "baseline_src.bin"
    hkd_src = work / "hkd_src.bin"

    print("HKD_SOCKET_1G_WAN_CLIENT")
    print("LABEL=NON_CHEAT_REAL_TCP_EXACT_TRACKED_UPDATE_BENCHMARK")
    print("host=%s port=%d" % (args.host, args.port))
    print("size_bytes=%d size=%s" % (size, human(size)))
    print("versions=%d" % versions)
    print("updates=%d" % (versions - 1))
    print("changed_bytes_per_update=%d changed=%s" % (changed, human(changed)))
    print("logical_full_retransmit_bytes=%d logical=%s" %
          (size * versions, human(size * versions)))

    # Mathematical ceiling before running anything.
    ideal_hkd_payload = size + (versions - 1) * changed
    ideal_ratio = (size * versions) / float(ideal_hkd_payload)
    print("ideal_hkd_literal_floor=%d ideal=%s" %
          (ideal_hkd_payload, human(ideal_hkd_payload)))
    print("ideal_payload_reduction_ceiling_x=%.6f" % ideal_ratio)
    print("NOTE=with a mandatory initial full snapshot, reduction_x cannot exceed versions")
    print()

    print("PREPARE_BASE", flush=True)
    make_base(base, size, args.seed)
    shutil.copyfile(base, baseline_src)
    shutil.copyfile(base, hkd_src)
    updates = make_updates(size, versions, changed, args.seed + 1)

    print("RUN_BASELINE", flush=True)
    b = run_baseline(args.host, args.port, baseline_src, updates)
    print("BASELINE tx_bytes=%d tx=%s elapsed_s=%.6f sha256=%s" %
          (b["tx"], human(b["tx"]), b["elapsed"], b["sha256"]), flush=True)

    print("RUN_HKD", flush=True)
    h = run_hkd(args.host, args.port, hkd_src, updates)
    print("HKD tx_bytes=%d tx=%s elapsed_s=%.6f active_bytes=%d "
          "active_ranges=%d sha256=%s" %
          (h["tx"], human(h["tx"]), h["elapsed"], h["active_bytes"],
           h["active_ranges"], h["sha256"]), flush=True)

    exact_same_source = (b["sha256"] == h["sha256"])
    payload_x = b["tx"] / float(h["tx"])
    time_x = b["elapsed"] / float(h["elapsed"]) if h["elapsed"] else float("inf")

    print()
    print("RESULT")
    print("same_final_source_sha256=%s" % exact_same_source)
    print("payload_reduction_x=%.6f" % payload_x)
    print("wall_clock_speedup_x=%.6f" % time_x)
    print("baseline_elapsed_s=%.6f" % b["elapsed"])
    print("hkd_elapsed_s=%.6f" % h["elapsed"])
    print("baseline_tx=%s" % human(b["tx"]))
    print("hkd_tx=%s" % human(h["tx"]))
    print("IMPORTANT=receiver stdout must show matching SHA256 for baseline and HKD outputs")
    print("PASS_CLIENT=%s" % exact_same_source)


def local(args):
    # Local correctness/performance mode; same code paths, loopback rather than WAN.
    server_args = argparse.Namespace(
        bind="127.0.0.1", port=args.port, out_dir=args.out_dir, runs=2
    )
    t = threading.Thread(target=server, args=(server_args,), daemon=True)
    t.start()
    time.sleep(0.2)
    c = argparse.Namespace(
        host="127.0.0.1", port=args.port, size_gib=args.size_gib,
        changed_mib=args.changed_mib, versions=args.versions,
        work_dir=args.work_dir, seed=args.seed
    )
    client(c)
    t.join()


def selftest_baseline():
    """Tiny real-TCP structural smoke test that does not require hkd_socket."""
    with tempfile.TemporaryDirectory(prefix="hkd_wan_selftest_") as td:
        td = Path(td)
        out = td / "out.bin"
        src = td / "src.bin"
        size = 2 << 20
        make_base(src, size, 123)
        updates = make_updates(size, 3, 4096, 456)

        ls = std_socket.socket(std_socket.AF_INET, std_socket.SOCK_STREAM)
        ls.setsockopt(std_socket.SOL_SOCKET, std_socket.SO_REUSEADDR, 1)
        ls.bind(("127.0.0.1", 0))
        ls.listen(1)
        port = ls.getsockname()[1]
        result = {}

        def r():
            conn, _ = ls.accept()
            try:
                result["receiver"] = receiver_one(conn, out, "selftest")
            finally:
                ls.close()

        t = threading.Thread(target=r, daemon=True)
        t.start()
        x = run_baseline("127.0.0.1", port, src, updates)
        t.join()
        ok = x["sha256"] == sha256_file(out)
        print("SELFTEST_BASELINE_REAL_TCP")
        print("bytes=%d versions=3 changed_per_update=4096 exact=%s tx=%d" %
              (size, ok, x["tx"]))
        if not ok:
            raise SystemExit("selftest failed")


def build_parser():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)

    s = sp.add_parser("server", help="run on WEST receiver")
    s.add_argument("--bind", default="0.0.0.0")
    s.add_argument("--port", type=int, default=5001)
    s.add_argument("--out-dir", default="/tmp/hkd_socket_west")
    s.add_argument("--runs", type=int, default=2)
    s.set_defaults(func=server)

    c = sp.add_parser("client", help="run on EAST sender")
    c.add_argument("--host", required=True)
    c.add_argument("--port", type=int, default=5001)
    c.add_argument("--size-gib", type=float, default=1.0)
    c.add_argument("--versions", type=int, default=100)
    c.add_argument("--changed-mib", type=float, default=1.0)
    c.add_argument("--work-dir", default="/tmp/hkd_socket_east")
    c.add_argument("--seed", type=int, default=20260812)
    c.set_defaults(func=client)

    l = sp.add_parser("local", help="same benchmark over Mac loopback")
    l.add_argument("--port", type=int, default=5001)
    l.add_argument("--size-gib", type=float, default=1.0)
    l.add_argument("--versions", type=int, default=100)
    l.add_argument("--changed-mib", type=float, default=1.0)
    l.add_argument("--work-dir", default="/tmp/hkd_socket_local")
    l.add_argument("--out-dir", default="/tmp/hkd_socket_local_recv")
    l.add_argument("--seed", type=int, default=20260812)
    l.set_defaults(func=local)

    q = sp.add_parser("selftest", help="tiny real-TCP baseline protocol smoke test")
    q.set_defaults(func=lambda args: selftest_baseline())
    return ap


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
