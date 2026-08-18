# -*- coding: utf-8 -*-
# HKD OBFUSCATE v4 - portable source payload, no marshal/code-object dependency.
# Protection is import-time only; protected functions have no per-call wrapper.
def _hkd_v4_bootstrap(_g):
    import binascii as _hb
    import hashlib as _hh
    import struct as _hs
    import zlib as _hz

    _b = (
        _hb.unhexlify('91f3c83a0dbcf13f7591ac2bdc674e7cfb4c05bbcd3be5caaf90cad7408ee144d15dc5f4edbc368470540a43124a72120730bc3d051e2412618139813678a9362366d82633925cc038bc3fa215689bdafe5292f0f07e3f815145de672a9ce6311066a1c5ed523f7e017c7fa4184ad9d1c9427260c0d9636877805f9ed4c74c70'),
        _hb.unhexlify('aa72656ffc8fdfc17f3015996c22a7be931937e5a9ef5e239b899c1ada97db0b946bb8af476cd15f1bdf78f9e4a2eae1cc6ba45b11770c8093b6a06f2cabc362cb6717308a6b785895268ac672c7315efeb2483fc5d761b3e008dd80c7b5639db88370d67bbd1bf32bb81d684a13dd680642d9572ee6a0bffafcc67e24e439c6'),
        _hb.unhexlify('2eaf431dfcd45e8fc349271ebd31bd3700415b4aefc565fefff7918a0221b97660f8ed0a8f0c313488cb542e9f95ea1a32c522a3416ca68828fdca9f08a8fae8b642702b4d7523eb79d4a7a631d74d4673d8aada6ec07388bfa07196b457e527201b53fddc02639b8e4f9b87c09714e42835fc235cf38e33b1678f4f8542bb63'),
        _hb.unhexlify('7dc2084ffbea7e638df6d8af153cdc4ea65f60d662ee48804531aa34b99d4ad05dfd9e8c026118a47dcc28d0dcbf1130756e5d1840f3b1b93a0995be92d666b410'),
    )
    _inv = (1, 0, 2, 3)
    _leaves = (
        _hb.unhexlify('f9eb1af8a016abe7ea8e31106abc3abc3d2b17c2070d194f29aff8e33c5a463d'),
        _hb.unhexlify('b3bb6aeeb44aa98aa3a2bffc60f35e18f297fbff408f06976f323a01e11ad229'),
        _hb.unhexlify('2101e83cb08e43d1745c042917b7416d43658fad19dd4a05f2137deb9df8c1be'),
        _hb.unhexlify('732a39a3d42f6aed6c943bae62ed5123286c11fb5efa8aae4ffb9e76af0a7bcc'),
    )
    _root = _hb.unhexlify('a20edbc97c1743bbe921ceb914393b069d4b599594fd0611d142c6263a7fa74b')
    _share1 = _hb.unhexlify('55eda5f163d89abc0fa9ee2f50360fb8a1798cbdee89b7724aa601d666ef165c')
    _share2 = _hb.unhexlify('9f79c9c5af812421529d38fa0edc11dc26853438e917cd18eb1ba098b56c4e3b')

    def _u32(_n):
        return _hs.pack('>I', _n)

    def _xor(_a, _c):
        _o = bytearray(len(_a))
        _i = 0
        while _i < len(_a):
            _o[_i] = _a[_i] ^ _c[_i]
            _i += 1
        return bytes(_o)

    def _ks(_key, _index, _length):
        _o = bytearray()
        _counter = 0
        _seed = _key + _u32(_index)
        while len(_o) < _length:
            _o.extend(_hh.sha256(_seed + _u32(_counter)).digest())
            _counter += 1
        return bytes(_o[:_length])

    def _merkle(_values):
        if not _values:
            return _hh.sha256(b'').digest()
        _level = list(_values)
        while len(_level) > 1:
            if len(_level) & 1:
                _level.append(_level[-1])
            _next = []
            _i = 0
            while _i < len(_level):
                _next.append(_hh.sha256(_level[_i] + _level[_i + 1]).digest())
                _i += 2
            _level = _next
        return _level[0]

    _key = _xor(_share1, _share2)
    _parts = []
    _verify = []
    _i = 0
    while _i < len(_inv):
        _masked = _b[_inv[_i]]
        _raw = _xor(_masked, _ks(_key, _i, len(_masked)))
        _parts.append(_raw)
        _verify.append(_hh.sha256(_u32(_i) + _raw).digest())
        _i += 1

    if tuple(_verify) != _leaves or _merkle(_verify) != _root:
        raise ImportError('HKD protected payload integrity verification failed')

    try:
        _source = _hz.decompress(b''.join(_parts)).decode('utf-8')
    except Exception as _exc:
        raise ImportError('HKD protected payload reconstruction failed: %s' % (_exc,))

    _filename = _g.get('__file__') or '<HKD-obfuscated>'
    _code = compile(_source, _filename, 'exec', 0, True, 0)

    # Discard the plaintext string before running user code.  CPython may reclaim
    # it immediately; no plaintext source is retained as a module global.
    del _source

    # Exact module semantics: definitions execute in the actual module globals.
    exec(_code, _g, _g)

_hkd_v4_bootstrap(globals())
del _hkd_v4_bootstrap
