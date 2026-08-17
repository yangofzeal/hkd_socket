# HKD∞ OBFUSCATE v3 — PYTHON-3.4-COMPATIBLE PROTECTED MODULE
# Source payload; no marshal/code-object version dependency.
# All protection work occurs once at import; protected calls have no wrapper.
import hashlib as _hh
import zlib as _hz

_B=(bytes.fromhex('345fd9d913a3443e90afe0e9e3a124264ccf9cd08311ea935845a6625dd33b96fe23e8447e55d96cad60b885c258728254d554cbc895da2ffe776a8477718db28d7cac7b7053f94e409bbbd7b50396f14590e9e9a9780d303d1430578108ab084001f3c1959a77233ba01fd4cb540fb7746c2b056683ac5ee994c03420c9c5a8'),
bytes.fromhex('f6219c9758a9564801e2ae6e6897d1afc0b32f081c7e26b63a5ddc0b1eae9541b4bc4d853815aa8ce399e24f726c1eded8a0aa6982a54760ab7edeb94f4bf42222d979a7fec2a2ae127033f4b8d2751855904b3068434ecf33c8b67fc0e8ffb1780dcae02df496132f89782e'),
bytes.fromhex('7ae908d9f0c36653bdaaf6a218645c2e710e65c77405ed1d214fc20d3377d7be47cf044851999220c5ca78f8c11645a450de84e11d4eaa3b828305e4b0f5f86282496b18419f071b3346d9267af49149a08501a519073ae404bbc9d2e1af0ec56f0a8c9aeb2040af254c333281e85b82619ca55665871a9c3298b89f3948761c'),
bytes.fromhex('98875ef097383b782085aaf4a741b261d518269fb65f6b13d07fd63d39f6b9883cce0e9e486dc853ee28b87b9224d5b4cbf015752d6df25445acf353c07876da34d28208d5efac5259fd46ca8cb6ebc4d926730a07b7b745dbd4c74fb6f92e0fe7102d127a4bfbb8f1e123454e3093bf4c4706478000452335be956cca1e3403'),
bytes.fromhex('27c92aba87d47ae722149c162a1d17670b1f977b3cd055af5683fe1eee4f5da43edd1ae8ba641159d4f255270a0fbf143af6c39c48f0c5f58d6a245cfd9dec95568dace74f0ef0afe26c6c6480886f3eecc0bd3d101270e05272ee4ba50c717337907f3e6537a5d387eb35ce42b1ee19cd177f967e70ab809c0ae9e1035a8835'),
bytes.fromhex('6efd0d6d9facec03adb2fe2348e3280c2d63740b5e5e9cbf752ca88bcc71bf26e41f14744049b546a87ce2cabf1648114cef46586b609eb644c5df0c3f986db357e060ddc8984865f14c8c6475dc991f44a061fca6e5957194b850318a65f14484c94512b07aa41b3243f29902b30e1ebc25af12407575d30920e4e943a1404d'),
bytes.fromhex('486d51bb77de6e5c7f6db23f0080d31c6adcec3500f1ff845420961d3bfdc406c6295efbe2fc1c5d8f2a3e34ecbb81eed9a178f923b44be925062d21e449c00bad31039551a42e797a969c69a03541623429d17167f3cc217ff7410905a37b9674eeacc76004cec65d8ec89a9496417c8c7402c2d5c038c5d3a8744c2181ce2e'),
bytes.fromhex('aa727d65c68adfc77bb22c71e61aa50e4c4c59d68cced09ea837123b1dbbf4af5aea431161bacc8def81ae47b6d9c0a6cc55063e255284cca0de3e77796bf23eec09fb921f92ca6b8b5259b8323bb30efb279d4a1d1c7d5b20f91ae67bb99e6b14a2872019d763af8d1b1a32f3aaae49382bc3c92f296253a84c594e58021337'),
bytes.fromhex('18b25af42cd2bfb7644d4d22b0516d9355d00981062a1a214bff4a955fe42749ce4da540b8f1a091f10c5b783980e8c19cb2ef54dc6249234bdfb2cf6169d3593395538ca2dcb0d53c7ecaaf93e42379728e53a90a02fde8794f688aa33790974662ddc81a172747168a10974d14185a577e5ff4754ed3ba82df107bd389e6eb'),
bytes.fromhex('71e1b71ba3287ef66be400589d2bc8b90a43ba767aedf4b732ac11ef80f38ca8ff6e7e6713f4756a68ca7094484d6ddf7a6720332d96b021ed679708dce315113dc6c8682d531e2c2c61531dd08dd6d8496ae968e7ebcd634ff77318f21e63d5770ca4497b062f4a71ea0ed5af7932f876a46d1ac24e785f00d236c295a85877'),
bytes.fromhex('610ce7046fca08a4ca58d1d182496d75afd252f5b102002b8a548ec36ca52e2d14402c201708d3419ddb1ae4439bf7a3a88e074915b8f1fa630c721c8ad72e89b5265622504f946aef410ac60363c4a6df709fcca735196d1869b383cf8088f92673f85a631a6fc190193c43266a8aa4bd16052ab0e9ff321fc68b0e054874b3'),
bytes.fromhex('5949d53a76c4b92cf84717d3df77ae930795b2480b644909f52325385af2dd0093b1514f848a6bc0ec22a25155b520f77cee0f4fac17b2f2f174cf9c6923fc55d5c35fb14f7e74b5602aaf17b6c6393c4fbec3fb529f8fa18eae3ec765f3220814fe5e8021d3dea6978a47f8906921f1ed181237894d8f7b99ae64e6dec73869'),
bytes.fromhex('21e21cb8d0e18138e3cc6639381f84d9d26c722364f820d7eec1fa9d5d9949a8045e3ee50e4259b1076b7303af9e8154dc69b524908fdb1b1268717a6b44a4b7bce1b8c871d65ebaf68831a8546800f482167a79e0f5cf0fc44840370894c9b0ab70b52892b69789998d07807be65824cbeb85bd826e87347d94e7228f5ffd03'),
bytes.fromhex('a670b0e665f8d7747a533240b6105b26d87c51ee2943bf21f754f9a722ddbbf2d02d713e4d6fac110fb2af54d93a01443ce11e472d33da45d9a1b7ee84b802924ad89ff89bca28ef2c23bbb26cfa1867a0996677e7fe98f176dbaca7cc33af960203aabf44dc43cf29eca37d21bf09b78b8b251f28d40495d4fac54825ae06a8'),)
_I=(7, 3, 0, 12, 5, 6, 10, 2, 9, 13, 11, 4, 8, 1)
_L=(bytes.fromhex('b4d795c29dd292b38873e8d4ca66c1a2d8acb9527a6dd28788f7a51ca552a321'),
bytes.fromhex('70292e16ccdbfc779eed2a2638fecdae4fbc46f129d37827d1c796de69b32211'),
bytes.fromhex('bbbc7a37c39fbc57c9ede2ec982d1e8393be3c95cd4a7d4131a5da1e625477a3'),
bytes.fromhex('ee40cb0aabe8c7d74c0ef4ad9a16b09d157a412e129c5018708c4c64528c7742'),
bytes.fromhex('d1039b6acaaf780baaa8a9e360218c33adb69a9ea947d82957609981496353d4'),
bytes.fromhex('f7b32245facf551c2f8e5e1f113c8ac0de1e6a111a485db63a7485adf26b32ec'),
bytes.fromhex('eec5afa8edad767f5e473c64f0c4306ccd6b08e858b1c7ffa079c17fd844f1df'),
bytes.fromhex('7f525b2fb2cca1665f8d70f2f3fa8b5d48d657f6b624061f9f4470470abddabb'),
bytes.fromhex('a2cf0e457aaf1923346bef268637e65c281ce292644c62297d6c7355a224cb8c'),
bytes.fromhex('da7d7a6ea73b62789924585d386283bd7a2ddd9539a2deb48388f9a7e4abca77'),
bytes.fromhex('f0df93e87d453e45a156153ec2b2df324c20453362518b3817420a2ffeca1059'),
bytes.fromhex('45d5c7ac7baec37bd85d76756cc5e4fd938f04d8cc8c9325ec20410584202411'),
bytes.fromhex('89226211d0ed1c540ee89be9d7d3418e7d67b60f7355a14084da84e6df80fd61'),
bytes.fromhex('288b67881130cf57fac7a694ca63058c8db8c44a1aa54b67ebd559ec5ad291de'),)
_R=bytes.fromhex('caffd552289dd4c845638e659ce0f40d35a132723022aedc3f451e19de80951f')
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
