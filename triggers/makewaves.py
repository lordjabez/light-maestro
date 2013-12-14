#!/usr/bin/env python

wavelist = []
for p in range(48):
    for s in range(24):
        wave = {'method': 'PUT', 'url': 'http://localhost:3520/scenes/_current'}
        wave['name'] = 'P{0:02}-S{1:02}'.format(p + 1, s + 1)
        wave['data'] = {'id': p * 24 + s}
        wavelist.append(wave)

import json
import struct

for wave in wavelist:

    reqdata = '\n'.join((wave['method'], wave['url'], json.dumps(wave['data'])))
    reqlen = len(reqdata)
    if reqlen % 2 == 1:
        reqdata += '\n'
        reqlen += 1

    filelen = 36 + 8 + reqlen

    riffchunk = struct.pack('<4sL4s', 'RIFF'.encode(), filelen, 'WAVE'.encode())
    fmtchunk = struct.pack('<4sL2H2L2H', 'fmt '.encode(), 16, 1, 1, 22050, 44100, 2, 16)
    datachunk = struct.pack('<4sL', 'data'.encode(), 0)
    reqchunk = struct.pack('<4sL', 'req '.encode(), reqlen) + reqdata.encode()

    with open(wave['name'] + '.wav', 'wb') as f:
        f.write(riffchunk + fmtchunk + datachunk + reqchunk)
