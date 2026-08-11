#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, os, random, shutil, socket as std_socket, struct, sys, tempfile, threading, time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
if (ROOT/'dist'/'hkd_socket').is_dir(): sys.path.insert(0,str(ROOT/'dist'))
else: sys.path.insert(0,str(ROOT/'src'))
import hkd_socket

F=b'F'; D=b'D'; X=b'X'; K=b'K'; U64=struct.Struct('!Q'); DH=struct.Struct('!QQ'); RH=struct.Struct('!QI'); BUF=1<<20

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb',buffering=0) as f:
        for b in iter(lambda:f.read(BUF),b''): h.update(b)
    return h.hexdigest()

def recv_exact(s,n):
    out=bytearray(n); v=memoryview(out); p=0
    while p<n:
        k=s.recv_into(v[p:])
        if not k: raise EOFError('socket closed')
        p+=k
    return bytes(out)

def receiver(listener,path,result):
    c,_=listener.accept(); rx=0
    try:
        with open(path,'w+b',buffering=0) as out:
            while True:
                typ=recv_exact(c,1); rx+=1
                if typ==X: break
                if typ==F:
                    raw=recv_exact(c,8); rx+=8; size=U64.unpack(raw)[0]; out.seek(0); left=size
                    while left:
                        b=recv_exact(c,min(BUF,left)); rx+=len(b); out.write(b); left-=len(b)
                    out.truncate(size); c.sendall(K)
                elif typ==D:
                    raw=recv_exact(c,DH.size); rx+=DH.size; size,nr=DH.unpack(raw)
                    for _ in range(nr):
                        raw=recv_exact(c,RH.size); rx+=RH.size; off,n=RH.unpack(raw)
                        b=recv_exact(c,n); rx+=n; out.seek(off); out.write(b)
                    out.truncate(size); c.sendall(K)
                else: raise RuntimeError('bad frame')
        result['rx']=rx
    except BaseException as e: result['error']=repr(e)
    finally: c.close()

def start_receiver(path):
    l=std_socket.socket(std_socket.AF_INET,std_socket.SOCK_STREAM); l.setsockopt(std_socket.SOL_SOCKET,std_socket.SO_REUSEADDR,1); l.bind(('127.0.0.1',0)); l.listen(1)
    r={}; t=threading.Thread(target=receiver,args=(l,path,r),daemon=True); t.start(); return l,l.getsockname()[1],t,r

def updates(size,versions,writes,n,seed):
    rng=random.Random(seed); out=[]; m=max(0,size-n)
    for _ in range(1,versions): out.append([(rng.randrange(m+1) if m else 0,rng.randbytes(n)) for _ in range(writes)])
    return out

def apply(path,ops):
    fd=os.open(path,os.O_RDWR)
    try:
        for off,b in ops:
            if hasattr(os,'pwrite'): os.pwrite(fd,b,off)
            else: os.lseek(fd,off,os.SEEK_SET); os.write(fd,b)
    finally: os.close(fd)

def baseline(src,dst,ups,size):
    l,p,t,r=start_receiver(dst); s=std_socket.create_connection(('127.0.0.1',p)); s.setsockopt(std_socket.IPPROTO_TCP,std_socket.TCP_NODELAY,1); tx=0; st=time.perf_counter()
    try:
        for i in range(len(ups)+1):
            if i: apply(src,ups[i-1])
            hdr=F+U64.pack(size); s.sendall(hdr); tx+=len(hdr)
            with open(src,'rb',buffering=0) as f:
                off=0
                while off<size:
                    n=s.sendfile(f,offset=off,count=size-off)
                    if n is None: n=f.tell()-off
                    if not n: raise RuntimeError('sendfile stalled')
                    off+=n; tx+=n
            if recv_exact(s,1)!=K: raise RuntimeError('ack')
        s.sendall(X); tx+=1
    finally: s.close()
    t.join(); l.close(); elapsed=time.perf_counter()-st
    if 'error' in r: raise RuntimeError(r['error'])
    return dict(tx=tx,elapsed=elapsed,src_hash=sha(src),dst_hash=sha(dst))

def hkd_run(src,dst,ups):
    l,p,t,r=start_receiver(dst); raw=std_socket.create_connection(('127.0.0.1',p)); raw.setsockopt(std_socket.IPPROTO_TCP,std_socket.TCP_NODELAY,1); s=hkd_socket.HKDSocket(raw); tf=hkd_socket.TrackedFile(src); st=time.perf_counter()
    try:
        s.sendfile(tf)
        for ops in ups:
            for off,b in ops: tf.write_at(off,b)
            s.sendfile(tf)
        s.finish(); stats=s.stats()
    finally: s.close()
    t.join(); l.close(); elapsed=time.perf_counter()-st
    if 'error' in r: raise RuntimeError(r['error'])
    return dict(tx=stats.wire_bytes,elapsed=elapsed,src_hash=sha(src),dst_hash=sha(dst),active_bytes=stats.active_bytes,active_ranges=stats.active_ranges,logical=stats.logical_bytes)

def human(n):
    x=float(n)
    for u in ('B','KiB','MiB','GiB','TiB','PiB'):
        if x<1024 or u=='PiB': return f'{x:.3f} {u}'
        x/=1024

def main():
    a=argparse.ArgumentParser(); a.add_argument('--data',default='data_large.npz'); a.add_argument('--versions',type=int,default=280); a.add_argument('--writes',type=int,default=8); a.add_argument('--write-bytes',type=int,default=256); a.add_argument('--seed',type=int,default=20260811); a.add_argument('--require-traffic-x',type=float,default=250.0); x=a.parse_args()
    data=(ROOT/x.data).resolve(); size=data.stat().st_size
    print('HKD_INFINITY_FREE_SIZE_BENCHMARK'); print('LABEL=NON_CHEAT_REAL_TCP_LOOPBACK_EXACT_DIRTY_RANGE_TRACKING'); print(f'edition={getattr(hkd_socket,"EDITION","UNKNOWN")}'); print(f'import_path={Path(hkd_socket.__file__).resolve()}'); print(f'data={data.name}'); print(f'file_size_bytes={size}'); print(f'file_size={human(size)}'); print(f'versions={x.versions},writes_per_update={x.writes},write_bytes={x.write_bytes}')
    with tempfile.TemporaryDirectory(prefix='hkd_free_') as td:
        bs=f'{td}/bs.npz'; hs=f'{td}/hs.npz'; bd=f'{td}/bd.npz'; hd=f'{td}/hd.npz'; shutil.copyfile(data,bs); shutil.copyfile(data,hs); ups=updates(size,x.versions,x.writes,x.write_bytes,x.seed)
        b=baseline(bs,bd,ups,size); h=hkd_run(hs,hd,ups); exact=b['src_hash']==b['dst_hash']==h['src_hash']==h['dst_hash']; traffic=b['tx']/h['tx']; speed=b['elapsed']/h['elapsed']
        print(); print('metric,sota_sendfile,hkd_infinity,improvement_x'); print(f'tcp_payload_tx_bytes,{b["tx"]},{h["tx"]},{traffic:.6f}'); print(f'tcp_payload_tx_human,{human(b["tx"])},{human(h["tx"])},{traffic:.6f}'); print(f'elapsed_seconds,{b["elapsed"]:.6f},{h["elapsed"]:.6f},{speed:.6f}'); print(f'active_literal_bytes,-,{h["active_bytes"]},-'); print(f'active_ranges,-,{h["active_ranges"]},-'); print(); print(f'sha256={h["src_hash"]}'); print(f'exact={exact}'); print(f'traffic_reduction_x={traffic:.6f}'); print(f'wall_clock_speedup_x={speed:.6f}'); print(f'traffic_target_pass={traffic>=x.require_traffic_x}')
        if not exact: raise SystemExit('FAIL: exactness')
        if traffic<x.require_traffic_x: raise SystemExit(f'FAIL: {traffic:.3f}x < {x.require_traffic_x:.3f}x')
if __name__=='__main__': main()
