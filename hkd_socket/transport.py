# -*- coding: utf-8 -*-
# HKD OBFUSCATE v4 - portable source payload, no marshal/code-object dependency.
# Protection is import-time only; protected functions have no per-call wrapper.
def _hkd_v4_bootstrap(_g):
    import binascii as _hb
    import hashlib as _hh
    import struct as _hs
    import zlib as _hz

    _b = (
        _hb.unhexlify('088c414346ba5a2a25154be2bb325fdb0fd11bae0a8884677d4f4b906f9bab038cfeb69b4e6147d5c148f8c533c024dc27a74d77ae7f6168820d75a1feac95da9b876e8ccb8dd574ce4a28a31992b1d360b809effd6c0531ebb27ada2f8309102a9b352801ad3e7c6c8f9a3a88ae6d4873dbb441a4ec755f4c19a532ff84b41b'),
        _hb.unhexlify('72119d7725c0259f5ab640ea177141dd7a2e26ad06e403945cda850826e7b773271e0abe2c3c2ce0314390d08da7157c902a1e45e4481fd996bd3ba18b428140f3a709609a2cc264caa73e00a2520ae41ef1bb291031b6339ff1852d6e58a176af2c4bda00635d1fb22abe23f32f8aa6a86342d621501a82e6bc7d3cf79e3f0c'),
        _hb.unhexlify('d1c6c95be0605c2323c0055efe39ba6c1a56b4f0c2b9e5d872a62f2a2fb89358438bc23ccaa197d14049affce52acfa8699fdc9fa60e5ce02bc0351bb6ab0d24365de0cb5bd8a529bed12cd8fb660055a057bde102ab9df6dfd2f20bcdb06de3e8a7796e8e03582a00c7c73ba7262d44fa037c06672a3b55b8ba3bcf2d62a769'),
        _hb.unhexlify('7e0d62e3c775262d7c84e374c2e7f79d195ebe016928d079ff630ec81b92ff08e532b3e0ca94cb5fcb0c87e748e76f48b4946abb401aa0137a277634943ac595fd2a0d3fc509c4a9a46e320db03e62d25d185988144abcc563c999beb73a200a48bf6996a77f181045b8d4000efa45cd878ac76aee55557a3208202d39c2bfd4'),
        _hb.unhexlify('b6c2a21479050b434ee6c14ee663cf6069e47f0c3a377a05eb42507401c3cfcafbfea7d2b91454305e6d57ee164604097af75aceda76bb224622911b716d470e51f15421bfba130ff843c83f66c0cb9f25109f257b71eeba3f5d6f893c3d641373e9de04d8ab2cc72f6d81b80a37275a9c32d67da229d0128a0b024333352216'),
        _hb.unhexlify('c6d16091cee396b27034b984d0f60fd75e2b871607b963e2023d9fc8406a3c5206d1919b8c5ceb69f3c515017cd2d46904eabde2ca0b14ca4f2b811dee2ce398fc0c3edfb0aa111d915e7a53a8b2264079e5c9f61f42cf5cb497fc27c527f3d53b0ae46104c4b4a6ad0a14a2454737111b1aa47606b5aba1a57cf3ed674765c3'),
        _hb.unhexlify('57e88338ffdca936425a6511f2b8f045e8cef5e2b606e2c597868fe6e37f63f252cd5d4a74b178c24f7a277156c3e2371056f73e0072fdfe1ad480a63430b7b70eb9811a97201f82a4374f22bd8aea21b374686c42b135142b99c91408e38573f20840c91a9b44631b018e0315713518f41274bdb007736cc99bac42be228d81'),
        _hb.unhexlify('9f603242dd0fa1514a83f7bc4c3f34972520d521ba75eaa30150ef833c44242d5cc7b4ce912522ef43d597000069fa314a8f809a7d19b2ec176d0446152f3f9923aa9841191c0df04b297406febba20a1fbc04f6494b8bc6d67d21556aed06649319c9eba685ab7d3bb83ed1440c766d8792b8fc7c7faeae5515f1c258db8a56'),
        _hb.unhexlify('b365ca0ef64445b55f81f15fcd1a399d4b604e5030b5fe60a6b8b961324d6c4a22586561c7dee799b2eda6bcad1d79d5b898fdea0487257f47c726f4f78519e894ee9c793544a6111ad34da1f7a2f8d66efcd4a26deafb25883b17adf869c956e9531dc08f32edac93c1b5d57edb430ddbee72ca263acbcee531713feb50f18d'),
        _hb.unhexlify('04cfa133f66605ce209b1917ffd9a81014d61ef30ca0ac11f6d8b8aa896a44ccac54f4a3a07616e2d36e03b7b1326553c97bbb93eec7e9607b0303493babefdca0d3ab8b55cf12c968e9df944c676743c0eae90fcdf0aac99a4aa8c63c3ac5eb6934f4588be77a5f17a49d75efdc8ac2a02972ca0e67f2dcd694287655e34dd7'),
        _hb.unhexlify('fd39f52c05832dcace29946804f122295687f8a8092b6400f43c7097c050f19f875e642f49cba8a52833982d8923f77e297108cf0f842307a83ae613d2e1109fbe24afa5c879ad6869f5e4e633b8a8e6393184af70321d228605ab434fb1ca6ed6dbf2934a8f8a1e5d9f1028cf61a9a6dfe30c6c7d740b2e97e240885b80313a'),
        _hb.unhexlify('dabb3eeeeb2c9df8bed611d1e38b509791c48d1e8e63f507bd45120e14a470c16bcdc10b750f21dbe58b2889084c76f6b8508c14e47a24b4a9bc726d68f7944daf8d0f5fe60f9ad021745ccb237672b64b06bfac74098849cf0a2b60884542f88c4b0ec5cf381e8381e3cfccf859897db77956a096bcba479a37f68c'),
        _hb.unhexlify('7b3e2180b2b7aa059319f8f7a684b292931ca2578898707f3e863d11cf2c6837b304317cf6271706f3bbb6fb6c0cb0e31ff9480d269faeaf044eb712e80a2e6d806c09ff9343061309a690cd5741305a87caa21800c9e080631fb4d49793ab3ba90b8f4700ca0ec1637a88d326a00be2ba07de1213f9d29d3b107dc0acef1b3b'),
        _hb.unhexlify('e40b8b4b40c71671b9884117d2f10273dbea960f518322d6a875444206405a3007df01a4ccbda57ab8e961c4072a44f55a6e8b6865d515c9bc05de3a10122aa7ae458045806b7a5ecf9913d4f01428b55b41bc4eafb08c0fa7e1acb1abc8db5969fdc436dc8e4c8c707a6c42d5eb1dc089298412433252336d19786d75e2b0c2'),
        _hb.unhexlify('0d13aeb014b497dc922f91427f1a9d5e0f9a083416106e7729531ce7db27408d4360bc2643254ab5f7bda0044b47a9c5282cb09b445301abf0d577b95a42e5b87b701f0b6f8c5434d5c55dc313c9384ef644011c7d5dd078b2caf9608689a8fd8ad935f26726697627a3b69984e196dce91e9904850686f6ed4fc679c3735457'),
        _hb.unhexlify('aa725565768ae7c77d331561047a9ae787e8b3ff171bdc0502885ce5b9b1edb93ad2a5aa94d6d91b9ff81fa751158328ce5f8ea2a1ad316979f2cb97399450c4b390a08ca104af138fb26ff89da0d37b1fbb9e4039fa6509d6af04360a59d46b0b2fe12d8c8f44c3d5c2a67d92d792baa9ea59b0bb861f87fbef31bc196ffdb3'),
        _hb.unhexlify('15071a41b03a3e8b3c214445c3b5fe6ea8baec1eb6b65d7e9123157552b96b68ecf3746cb0d4eb0d67c16e219d39c2f9ac3d34447afb47c22653c52a4a5246eee94f783e102d1cbc7402526ca6db76d7148e6bc24db72de5d230896890d9d0e375bbd8673534e0fac86e6a4de2a5c778ada7dced2f0ca324f2408a05f60bd432'),
    )
    _inv = (15, 1, 16, 13, 14, 6, 10, 4, 3, 2, 5, 8, 0, 9, 7, 12, 11)
    _leaves = (
        _hb.unhexlify('ee71516facaf8cde92a8f5e4c57ba1b6344fae6d62d9e17e2d0dd7a55b13e479'),
        _hb.unhexlify('38f9ad94e3c9842030787173c77716d7c08811e88a2697e6abc3890903a385b6'),
        _hb.unhexlify('7e1cbd73153150269653fb461ff78da44c817cc353a1b4149678a27a50c1b8bc'),
        _hb.unhexlify('402e62084184fb245fd5cbd13c99425b1bbf59fff5e8840941b13257bd4c0a1d'),
        _hb.unhexlify('98769e77187c006bb9e9131dcece95a620932fbaee5f896a4760b6117ae3e13d'),
        _hb.unhexlify('0a082c6c2243df566e0c0c3134c7f420a9d2d16de20193e779ccc97acdf3dd00'),
        _hb.unhexlify('af2cfc218be77e977a979a03acc222b228d8da0604bd54c5d4d7cda63387c7da'),
        _hb.unhexlify('ea911091cdb477531c12aed1906315549530f86a5745f92728b0ea9e3dc70573'),
        _hb.unhexlify('380910ee992e8c834171491f05b41dab187a46761624e6f0a99bda4ba1980f33'),
        _hb.unhexlify('fdb944c5d99fbb26bea8da445b3051a1124443705c0111e8e2283cea6a2edae9'),
        _hb.unhexlify('8d38342ce7a918cc42f465d8912549835e7adfc0a2c2afa459db7b78a4aa5d16'),
        _hb.unhexlify('b5363447003bcb229724ceb51969336c1df3c75ae0606fe430a56d80d85550c5'),
        _hb.unhexlify('0cbae08ac3d9106e901417015f75ee22f2d9904c252ec9dbdbde76631a247f64'),
        _hb.unhexlify('54cd9a72a55dc3b689e1d3a305cbf33d0372f44be2aba8eae2ff5da2b0b12695'),
        _hb.unhexlify('7a15b0882cae51097c01b7fca81bf6ee3e6281a93f6cffda1bf86d9af8d810fa'),
        _hb.unhexlify('d0aea1ab4c78cddd5a7e5a69cfcffc7cf8d3eb50a4da5edd20293947c039e00b'),
        _hb.unhexlify('147ad4f8220b91343badb356b8bf641256bc6380b226c8ac512be2495dd17093'),
    )
    _root = _hb.unhexlify('630f723d26ce75efc8bd77c84c647d924f71d78a5a5cf86ba2e9802c0bc683f5')
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
