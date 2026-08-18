#!/usr/bin/env python3
from __future__ import print_function

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

ROOT = os.path.dirname(os.path.abspath(__file__))

# Prefer the package beside the test. Fall back to src/ or dist/ only if present.
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

src_dir = os.path.join(ROOT, 'src')
dist_dir = os.path.join(ROOT, 'dist')
if os.path.isdir(os.path.join(dist_dir, 'hkd_socket')):
    sys.path.insert(0, dist_dir)
elif os.path.isdir(os.path.join(src_dir, 'hkd_socket')):
    sys.path.insert(0, src_dir)

import hkd_socket

F = b'F'
D = b'D'
X = b'X'
K = b'K'
U64 = struct.Struct('!Q')
DH = struct.Struct('!QQ')
RH = struct.Struct('!QI')
BUF = 1 << 20


def sha(path):
    h = hashlib.sha256()
    f = open(path, 'rb', buffering=0)
    try:
        while True:
            b = f.read(BUF)
            if not b:
                break
            h.update(b)
    finally:
        f.close()
    return h.hexdigest()


def recv_exact(s, n):
    out = bytearray(n)
    v = memoryview(out)
    p = 0
    while p < n:
        k = s.recv_into(v[p:])
        if not k:
            raise EOFError('socket closed')
        p += k
    return bytes(out)


def receiver(listener, path, result):
    c, _ = listener.accept()
    rx = 0
    try:
        out = open(path, 'w+b', buffering=0)
        try:
            while True:
                typ = recv_exact(c, 1)
                rx += 1

                if typ == X:
                    break

                if typ == F:
                    raw = recv_exact(c, 8)
                    rx += 8
                    size = U64.unpack(raw)[0]
                    out.seek(0)
                    left = size
                    while left:
                        b = recv_exact(c, min(BUF, left))
                        rx += len(b)
                        out.write(b)
                        left -= len(b)
                    out.truncate(size)
                    c.sendall(K)

                elif typ == D:
                    raw = recv_exact(c, DH.size)
                    rx += DH.size
                    size, nr = DH.unpack(raw)

                    for _ in range(nr):
                        raw = recv_exact(c, RH.size)
                        rx += RH.size
                        off, n = RH.unpack(raw)
                        b = recv_exact(c, n)
                        rx += n
                        out.seek(off)
                        out.write(b)

                    out.truncate(size)
                    c.sendall(K)

                else:
                    raise RuntimeError('bad frame')
        finally:
            out.close()

        result['rx'] = rx

    except BaseException as e:
        result['error'] = repr(e)
    finally:
        c.close()


def start_receiver(path):
    listener = std_socket.socket(std_socket.AF_INET, std_socket.SOCK_STREAM)
    listener.setsockopt(std_socket.SOL_SOCKET, std_socket.SO_REUSEADDR, 1)
    listener.bind(('127.0.0.1', 0))
    listener.listen(1)

    result = {}
    t = threading.Thread(target=receiver, args=(listener, path, result))
    t.daemon = True
    t.start()

    return listener, listener.getsockname()[1], t, result


def random_bytes(rng, n):
    # random.Random.randbytes() does not exist on Python 3.4.
    return bytes(bytearray(rng.getrandbits(8) for _ in range(n)))


def updates(size, versions, writes, n, seed):
    rng = random.Random(seed)
    out = []
    m = max(0, size - n)

    for _ in range(1, versions):
        ops = []
        for _ in range(writes):
            off = rng.randrange(m + 1) if m else 0
            ops.append((off, random_bytes(rng, n)))
        out.append(ops)

    return out


def apply(path, ops):
    fd = os.open(path, os.O_RDWR)
    try:
        for off, b in ops:
            if hasattr(os, 'pwrite'):
                os.pwrite(fd, b, off)
            else:
                os.lseek(fd, off, os.SEEK_SET)
                os.write(fd, b)
    finally:
        os.close(fd)


def send_file_compat(sock, path, size):
    # socket.socket.sendfile() was added after Python 3.4.
    sent_total = 0
    f = open(path, 'rb', buffering=0)
    try:
        while sent_total < size:
            b = f.read(min(BUF, size - sent_total))
            if not b:
                raise RuntimeError('source shortened during baseline send')
            sock.sendall(b)
            sent_total += len(b)
    finally:
        f.close()
    return sent_total


def baseline(src, dst, ups, size):
    listener, port, t, result = start_receiver(dst)
    s = std_socket.create_connection(('127.0.0.1', port))
    s.setsockopt(std_socket.IPPROTO_TCP, std_socket.TCP_NODELAY, 1)

    tx = 0
    st = time.perf_counter()

    try:
        for i in range(len(ups) + 1):
            if i:
                apply(src, ups[i - 1])

            hdr = F + U64.pack(size)
            s.sendall(hdr)
            tx += len(hdr)
            tx += send_file_compat(s, src, size)

            if recv_exact(s, 1) != K:
                raise RuntimeError('ack')

        s.sendall(X)
        tx += 1

    finally:
        s.close()

    t.join()
    listener.close()
    elapsed = time.perf_counter() - st

    if 'error' in result:
        raise RuntimeError(result['error'])

    return {
        'tx': tx,
        'elapsed': elapsed,
        'src_hash': sha(src),
        'dst_hash': sha(dst)
    }


def hkd_run(src, dst, ups):
    listener, port, t, result = start_receiver(dst)
    raw = std_socket.create_connection(('127.0.0.1', port))
    raw.setsockopt(std_socket.IPPROTO_TCP, std_socket.TCP_NODELAY, 1)

    s = hkd_socket.HKDSocket(raw)
    tf = hkd_socket.TrackedFile(src)
    st = time.perf_counter()

    try:
        s.sendfile(tf)

        for ops in ups:
            for off, b in ops:
                tf.write_at(off, b)
            s.sendfile(tf)

        s.finish()
        stats = s.stats()

    finally:
        s.close()

    t.join()
    listener.close()
    elapsed = time.perf_counter() - st

    if 'error' in result:
        raise RuntimeError(result['error'])

    return {
        'tx': stats.wire_bytes,
        'elapsed': elapsed,
        'src_hash': sha(src),
        'dst_hash': sha(dst),
        'active_bytes': stats.active_bytes,
        'active_ranges': stats.active_ranges,
        'logical': stats.logical_bytes
    }


def human(n):
    x = float(n)
    for u in ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB'):
        if x < 1024 or u == 'PiB':
            return '%.3f %s' % (x, u)
        x /= 1024.0


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--data', default='data_free.npz')
    a.add_argument('--versions', type=int, default=280)
    a.add_argument('--writes', type=int, default=8)
    a.add_argument('--write-bytes', type=int, default=256)
    a.add_argument('--seed', type=int, default=20260811)
    a.add_argument('--require-traffic-x', type=float, default=250.0)
    x = a.parse_args()

    data = os.path.abspath(os.path.join(ROOT, x.data))
    size = os.path.getsize(data)

    print('HKD_INFINITY_FREE_SIZE_BENCHMARK')
    print('LABEL=NON_CHEAT_REAL_TCP_LOOPBACK_EXACT_DIRTY_RANGE_TRACKING')
    print('edition=%s' % getattr(hkd_socket, 'EDITION', 'UNKNOWN'))
    print('import_path=%s' % os.path.abspath(hkd_socket.__file__))
    print('data=%s' % os.path.basename(data))
    print('file_size_bytes=%d' % size)
    print('file_size=%s' % human(size))
    print('versions=%d,writes_per_update=%d,write_bytes=%d' %
          (x.versions, x.writes, x.write_bytes))

    td = tempfile.mkdtemp(prefix='hkd_free_')
    try:
        bs = os.path.join(td, 'bs.npz')
        hs = os.path.join(td, 'hs.npz')
        bd = os.path.join(td, 'bd.npz')
        hd = os.path.join(td, 'hd.npz')

        shutil.copyfile(data, bs)
        shutil.copyfile(data, hs)

        ups = updates(size, x.versions, x.writes, x.write_bytes, x.seed)
        b = baseline(bs, bd, ups, size)
        h = hkd_run(hs, hd, ups)

        exact = (
            b['src_hash'] == b['dst_hash'] ==
            h['src_hash'] == h['dst_hash']
        )
        traffic = float(b['tx']) / float(h['tx'])
        speed = float(b['elapsed']) / float(h['elapsed'])

        print()
        print('metric,sota_sendfile,hkd_infinity,improvement_x')
        print('tcp_payload_tx_bytes,%d,%d,%.6f' %
              (b['tx'], h['tx'], traffic))
        print('tcp_payload_tx_human,%s,%s,%.6f' %
              (human(b['tx']), human(h['tx']), traffic))
        print('elapsed_seconds,%.6f,%.6f,%.6f' %
              (b['elapsed'], h['elapsed'], speed))
        print('active_literal_bytes,-,%d,-' % h['active_bytes'])
        print('active_ranges,-,%d,-' % h['active_ranges'])
        print()
        print('sha256=%s' % h['src_hash'])
        print('exact=%s' % exact)
        print('traffic_reduction_x=%.6f' % traffic)
        print('wall_clock_speedup_x=%.6f' % speed)
        print('traffic_target_pass=%s' % (traffic >= x.require_traffic_x))

        if not exact:
            raise SystemExit('FAIL: exactness')

        if traffic < x.require_traffic_x:
            raise SystemExit(
                'FAIL: %.3fx < %.3fx' %
                (traffic, x.require_traffic_x)
            )

    finally:
        shutil.rmtree(td, ignore_errors=True)


if __name__ == '__main__':
    main()
