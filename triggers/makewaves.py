#!/usr/bin/env python


import struct


wavelist = []
for s in range(12):
    wave = {'method': 'POST'}
    wave['url'] = 'http://localhost:3520/scenes/{0}/_load'.format(s + 1)
    wave['name'] = 'Scene {0:02}'.format(s + 1)
    wave['data'] = ''
    wavelist.append(wave)


for wave in wavelist:

    reqdata = '\n'.join((wave['method'], wave['url'], wave['data']))
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
