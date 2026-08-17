# HKD∞ OBFUSCATE v3 — PYTHON-3.4-COMPATIBLE PROTECTED MODULE
# Source payload; no marshal/code-object version dependency.
# All protection work occurs once at import; protected calls have no wrapper.
import hashlib as _hh
import zlib as _hz

_B=(bytes.fromhex('91f3c83a0dbcf13f7591ac2bdc674e7cfb4c05bbcd3be5caaf90cad7408ee144d15dc5f4edbc368470540a43124a72120730bc3d051e2412618139813678a9362366d82633925cc038bc3fa215689bdafe5292f0f07e3f815145de672a9ce6311066a1c5ed523f7e017c7fa4184ad9d1c9427260c0d9636877805f9ed4c74c70'),
bytes.fromhex('aa72656ffc8fdfc17f3015996c22a7be931937e5a9ef5e239b899c1ada97db0b946bb8af476cd15f1bdf78f9e4a2eae1cc6ba45b11770c8093b6a06f2cabc362cb6717308a6b785895268ac672c7315efeb2483fc5d761b3e008dd80c7b5639db88370d67bbd1bf32bb81d684a13dd680642d9572ee6a0bffafcc67e24e439c6'),
bytes.fromhex('2eaf431dfcd45e8fc349271ebd31bd3700415b4aefc565fefff7918a0221b97660f8ed0a8f0c313488cb542e9f95ea1a32c522a3416ca68828fdca9f08a8fae8b642702b4d7523eb79d4a7a631d74d4673d8aada6ec07388bfa07196b457e527201b53fddc02639b8e4f9b87c09714e42835fc235cf38e33b1678f4f8542bb63'),
bytes.fromhex('7dc2084ffbea7e638df6d8af153cdc4ea65f60d662ee48804531aa34b99d4ad05dfd9e8c026118a47dcc28d0dcbf1130756e5d1840f3b1b93a0995be92d666b410'),)
_I=(1, 0, 2, 3)
_L=(bytes.fromhex('f9eb1af8a016abe7ea8e31106abc3abc3d2b17c2070d194f29aff8e33c5a463d'),
bytes.fromhex('b3bb6aeeb44aa98aa3a2bffc60f35e18f297fbff408f06976f323a01e11ad229'),
bytes.fromhex('2101e83cb08e43d1745c042917b7416d43658fad19dd4a05f2137deb9df8c1be'),
bytes.fromhex('732a39a3d42f6aed6c943bae62ed5123286c11fb5efa8aae4ffb9e76af0a7bcc'),)
_R=bytes.fromhex('a20edbc97c1743bbe921ceb914393b069d4b599594fd0611d142c6263a7fa74b')
_S1=bytes.fromhex('b4c44a1d49f84630e6a3d8f9e940b5fe9bac91bad310595a9d955dd8b13e68ff')
_S2=bytes.fromhex('7e50262985a1f8adbb970e2cb7aaab9a1c50293fd48e23303c28fc9662bd3098')

def _x(a,b):
    return bytes(i^j for i,j in zip(a,b))

def _n4(n):
    return n.to_bytes(4,'big')

def _ks(k,idx,n):
    o=bytearray(); c=0; s=k+_n4(idx)
    while len(o)<n:
        o.extend(_hh.sha256(s+_n4(c)).digest()); c+=1
    return bytes(o[:n])

def _mr(v):
    if not v:
        return _hh.sha256(b'').digest()
    v=list(v)
    while len(v)>1:
        if len(v)&1: v.append(v[-1])
        v=[_hh.sha256(v[i]+v[i+1]).digest() for i in range(0,len(v),2)]
    return v[0]

_K=_x(_S1,_S2)
_P=[]
_V=[]
for _i in range(len(_I)):
    _m=_B[_I[_i]]
    _r=_x(_m,_ks(_K,_i,len(_m)))
    _P.append(_r)
    _V.append(_hh.sha256(_n4(_i)+_r).digest())
if tuple(_V)!=_L or _mr(_V)!=_R:
    raise ImportError('HKD∞ SHA-256 integrity verification failed')

try:
    _S=_hz.decompress(b''.join(_P)).decode('utf-8')
except (ValueError, UnicodeDecodeError, _hz.error):
    raise ImportError('HKD∞ protected payload reconstruction failed')

_G=globals()
_N={
    '__name__':_G.get('__name__'),
    '__doc__':_G.get('__doc__'),
    '__package__':_G.get('__package__'),
    '__loader__':_G.get('__loader__'),
    '__spec__':_G.get('__spec__'),
    '__file__':_G.get('__file__'),
    '__cached__':_G.get('__cached__'),
    '__builtins__':_G.get('__builtins__'),
}
_C=compile(_S,_G.get('__file__') or '<HKD-obfuscated>','exec',0,True,0)
exec(_C,_N,_N)

for _q,_v in list(_N.items()):
    if _q != '__builtins__':
        _G[_q]=_v

# Functions retain _N as their normal globals dictionary. Remove loader-only names
# from the actual module namespace without mutating _N after source execution.
del _B,_I,_L,_R,_S1,_S2,_K,_P,_V,_S,_C,_i,_m,_r,_x,_n4,_ks,_mr,_q,_v,_N,_G,_hh,_hz
