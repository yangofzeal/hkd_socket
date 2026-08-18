# -*- coding: utf-8 -*-
# HKD OBFUSCATE v4 - portable source payload, no marshal/code-object dependency.
# Protection is import-time only; protected functions have no per-call wrapper.
def _hkd_v4_bootstrap(_g):
    import binascii as _hb
    import hashlib as _hh
    import struct as _hs
    import zlib as _hz

    _b = (
        _hb.unhexlify('6ad8edb47f0bf85b8a34f42e122fc9ac3dbcb1bdc8f118b76eac0baac0d17bae1de030a05fcbf99c9b766ce850e57f0876789bc358829c0b89e5e8b96a22a667ce204e32bfd7b108610bc29ca976b33da91591d2175f5fd70d6ef970ffd50a31fcef680ae2e2d41b747985d6678e8380202153f0f476dcedd666703aa731fc27'),
        _hb.unhexlify('d77518ed41e7f35b5370085be36e3bd5eabb6b94d9bc8a2457a55ba31161fa7ee02f3f9b8ae0c63f83aede2038d96f8f9babb9cc9930b76eba30cacb89e6ef9f97069331579e4d9c10760b88fd3af848566467d492e1cc53d20f982490c3884b9e797fe1f1db87e16797f3ca431e1522d63a4dc6ddc4ba56fcf36e3ca33139c5'),
        _hb.unhexlify('09f5658f21b491edc23dbe11f2771d8f23855ce8e54961faa24ce98aaefc0a4055b1020bc806fbd3a6c808f366d801b57049af752b00f7d577a575c55f1dc2282b1baab55c652dd0ea7f49b853ee69cd7749810e400c21a94bc1d652005dfcc1b952f4b25898e81e4fc54abc35d230b654c294e4a611f56ae1686ad8db78b5f8'),
        _hb.unhexlify('bf8e026d901ee0b607960f489b6ebbdc57dd9683e5bef7dd58e72d1147a2336197783033cb14e92e369c69a0219618c42de5753882c9aaa4dcaed3bcff65cdf7885649f90e65bef4fe51fcfb4dd446d1f27a3631d64196a98c50009b45f0664178be1bb843ded36216fba28c680254ece1f4365add0bcda27edbc34ef421b444'),
        _hb.unhexlify('5aade91dd8c426d9b9824d8d25cabb5bb992e7c669586065d26cbea1021455fe4027e3a66232ac0487818a23c5706688b551affc37bbf7c031f4a7e16ed41692988b38e8db160f6f5cecc2c22f2b5661733402b92097591b091a232b4e03ccc5ef3319603993d65eb580e440f5d776f1e09aed3baeb970af24b0dbac801f3bc4'),
        _hb.unhexlify('19372c2f2dd916875e4d42b8161c6538dc03096c1e83efb4618206bd422f86a02bd8cff53ecc6b8a3f47a3672603e6862e1ad3f64ef27d98dcbc70239ccf6d6742e3d553476be07815c789270043cb14f69a5908d0067fbb86fe66cf819692457f8ce4b844daa07fb7e013d91c19d60c28f5ea525710eb9cec8e7002481b19ff'),
        _hb.unhexlify('7e7c6a97436e7b80cbbeb56e4103a1492ba43124a26bc84dabe427a8fd39e082dcf2af294777c050aac507a2832404e8c4cf470940d762995f9e031bfeb1b86b080b56f90a5b5a2cca74021d6994dc489dcb3c95bb67c8c66353ec1c7ed864c4b547ac6065157f1ffb46b5c41c73f3d658b9ce245e9b11c83468cc79053526d4'),
        _hb.unhexlify('f887a88b582a0fda8cac581dcaab3106d92192aa1fa19f009edcdc4cbb5f01f9b1a141ab0ce90f669d02c76948755fdf291f6befdd8d646d6bcc7686a7ae80f3a2dedfaf17cb02f752e07e312e46fde62a9087407c2cc46eb91cfc15ddaa1c7934d394c3d5405681836dbc78c8cd5aa4572ad9516a9e69aa31e8ae97c8240cd1'),
        _hb.unhexlify('c961947dc61837899fd7c40554fa89865df4f6f68daed328fad91b4243a232b80b6f95282ab30d1e93071f52b33d670018ff17dba2ad2837f9a99963e02045d6bb1cb1a82b889564e3c6a48f83d1e0f0aa96004adf5ddef75c7b7939b7cead078f2ed3a11683d719c1a78af7e2e5562c486be5c891109585cb3a4cff0cff04f7'),
        _hb.unhexlify('b6476e89bb1bc0a7f958088e9e73d6ef6d14b3d61392aed65074fce9956ec586abf8875728accfc5266e77a78eaec6900aeb280a54da5ec43b8fb69c0771b416f19b15ed6a82c50627e453fcab2745aff44fd884e1154e9237386632c9f28db7af012d056fe8ae1a13b8e8b2039c0e2d8ffa2d4194a4a577ac7ff70905fb74a4'),
        _hb.unhexlify('2500bc918e65dadb5ae30ab4ac004976d633d2e7bfba83cf223cf8bd12d81c38be0104df44e340a2540c363ff1c9e90da98d1e2638b8298ecf7f4915efac0c01336f9bb5e034e4455d724ed377b271dc32ad48c443862360d901ab0090b8dda9e0ac108bcc5bb0deccac79102bf6d81f953ca2d54e01afcf35e8fad48ccae388'),
        _hb.unhexlify('e76b890eca34c6ac1a'),
        _hb.unhexlify('4295858b7e155b3d8045f37c225d91e934d19ce73e39ce6b370bea38b22488c041b633ba7b888ef392abf19a04d4b79d48bc9852724886568c53fa0987753e40fa7588b6064052555556f11784dc9f62d601d814c57d3fe559c7abbe4f455995f225f966eac88ffdc8ecc45044264c3f2c2b12233f029ab4861f5367492f9ad5'),
        _hb.unhexlify('3bbdfb2c0a2f141ebb1cb340e87e5e3b25d46729d870a8b81908fe856514d837fafa6c589d42219e4c107d9a72f736d03678f29c761adca4db1edd5da060cded073cfc025b14f545adc9264612f1c96e2b6be1554ef54e5bd5d5752d0e43ccc3f0e1c208a580a46f70f0ad894bd3831ece017f7306e34b1922bdda2cafd9e171'),
        _hb.unhexlify('84fb78f0433da1774f97811817d5dc860f49bf83229cafe9155638c4d90c4bec8c732a50e3c914992c6d2c7d5f8c05cea1366c2f4aa6aafa995d1b0a200eadffd6f30d1aa26e674ab2250ba39313e77f4ee7670e4b5ae9bfc9f90ef0bbde74baf4a7d93633981c7db0ae155ac97d3503e7a3af0a60707e44fea4e69ae11aab37'),
        _hb.unhexlify('b44c0dc96ef5757f9733e32da41977a43732172c6d5f7aa91faddadf70ab3f10075b4292a5640027f2929a2f310e7cda4ac914ff89cfd886df5e55ec59cafc2d3bbb0072337672c02f3eba2c2bf31ce1a38579110402db8f2b083b637e4fd2ceea6404a5dbe9e8352f8130ee2b053b1a58d8f8c71e6fb4ae048d5d65f2f4114c'),
        _hb.unhexlify('9f6a3bb6b5c18837ac337b29deb72098ba2f5cafd9e3830c2a9cb872ac4f37feab5e8d1f20b7f64295ba13b91325f681195c9543abc53f9130c8f54c0d9fdbe5fbd9e3655240355184f3d552be755e69ff7e5b848521550180046b7147d6d96bc1aa24e319af00c0f790b48812c54ff8533203909b3c2a93988f67191ab68b9b'),
        _hb.unhexlify('aa725565c68adf477db26c71e61cc7a6b4a16969217952372328e9f3ce05949acb594f0ed1742558bc5c17da369dbfae66cd5dd18776192c1dcbca87a259d7be762c1c138e1bc366b281f747e2fd4562950095b6f1477cedd675c55b53c3f6f9bf522d067ed7b1825a084699c8219866f899aefcc29efc7232d22272dc2c2557'),
    )
    _inv = (17, 12, 2, 15, 1, 13, 16, 6, 10, 14, 8, 3, 0, 9, 4, 7, 5, 11)
    _leaves = (
        _hb.unhexlify('026984900fbc4aca73f28e3122caf8096b0c982b457724cec2317374cf921166'),
        _hb.unhexlify('bdd1ae11d6a661d3125c7bddac2a1ea64557985627900f453290b5d2eb27c6fa'),
        _hb.unhexlify('23d81f4b6e51aee0ab9fa1e049f77f091a10106cdbf361772a3cc3ad51c763d7'),
        _hb.unhexlify('88e224fd0653b5c7692997e1f48447cb39ca969ffa309d2edd61a4c72ff5ba68'),
        _hb.unhexlify('78ca83bcd37b07ccf31ae423e454b7414aa192a31d9408683d822003838e035e'),
        _hb.unhexlify('9c62acbd452152008b1dff093869e9e8718e661f2e33202f85b51edaaf467d38'),
        _hb.unhexlify('e12ae34183723fe55140117c5edb161c04dc6d1c101bdb345c2a817862426125'),
        _hb.unhexlify('948cbce8a5681b9ee0b3d3dfb5aafd5f378a89e6d73cdc601a154bdd51321327'),
        _hb.unhexlify('2305b226df11d939b1f121721a6e76e2537b574b2cce2cd624cd1e77b5204b4e'),
        _hb.unhexlify('da4f6275bda10f3422e0c47be3b45cea9ba525e6fbeabdd8bdea8f5b2acde079'),
        _hb.unhexlify('633bdeadad49a8824c1ee5d259815b32c33e781513f2ca06eb9068e803fdb228'),
        _hb.unhexlify('6bcccca0680cbc36999aae07113d39a523af4ee46b418cb95c8ba02700773fec'),
        _hb.unhexlify('371abd6e3b55374a79a37e975e36b28edc4f2681823b2367c8584353fda1739d'),
        _hb.unhexlify('46a1172ea9540d66155fbf37300a2ccf17b9ffa67f88bb80cb1b546b8b00856a'),
        _hb.unhexlify('4c9d17539fe5b285242cdba761cfdb64a3fe25bed5e63e074f2513b0e0c791c0'),
        _hb.unhexlify('b5fc4808f464cb311a87bbb9a6dfb6e25b4f39ff4298a3dc4c56949f011d755f'),
        _hb.unhexlify('31d68e35af1ecd9f40d4ff97a7546132fc1e9b513fa350319cfaef7facd40d19'),
        _hb.unhexlify('acd5dd6aa3922e2b7d94adbe60577c2a1ed8417e6fe8fba798e56fc475c1949f'),
    )
    _root = _hb.unhexlify('6c658629660855e0ef068c45e2d4f21d233a3953dad06216df9e24b5cff5d7f1')
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
