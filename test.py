#!/usr/bin/env python3
import os, socket as std_socket, struct, sys, threading
from pathlib import Path
ROOT=Path(__file__).resolve().parent
if (ROOT/'dist'/'hkd_socket').is_dir(): sys.path.insert(0,str(ROOT/'dist'))
else: sys.path.insert(0,str(ROOT/'src'))
import hkd_socket
U64=struct.Struct('!Q')

def recv_exact(c,n):
    out=bytearray(n); v=memoryview(out); p=0
    while p<n:
        k=c.recv_into(v[p:])
        if not k: raise EOFError
        p+=k
    return bytes(out)

def server(listener,result):
    c,_=listener.accept()
    try:
        typ=recv_exact(c,1)
        if typ==b'F':
            size=U64.unpack(recv_exact(c,8))[0]
            left=size
            while left:
                b=c.recv(min(1<<20,left))
                if not b: raise EOFError
                left-=len(b)
            c.sendall(b'K'); result['received']=size
    except EOFError:
        result['closed_before_frame']=True
    finally: c.close()

p=ROOT/'data_large.npz'
print('HKD_SOCKET_LARGE_FILE_LICENSE_TEST')
print(f'edition={getattr(hkd_socket,"EDITION","UNKNOWN")}')
print(f'import_path={Path(hkd_socket.__file__).resolve()}')
print(f'file={p.name}')
print(f'file_size_bytes={os.path.getsize(p)}')
l=std_socket.socket(); l.bind(('127.0.0.1',0)); l.listen(1); result={}
t=threading.Thread(target=server,args=(l,result),daemon=True); t.start()
raw=std_socket.create_connection(l.getsockname())
s=hkd_socket.HKDSocket(raw)
try:
    tf=hkd_socket.TrackedFile(str(p))
    try:
        s.sendfile(tf)
        print('result=ALLOWED')
        print(f'received_bytes={result.get("received",os.path.getsize(p))}')
    except RuntimeError as e:
        print(f'ERROR: {e}')
        print('result=PAID_REQUIRED')
finally:
    try: s.close()
    except Exception: pass
    l.close(); t.join(timeout=3)
