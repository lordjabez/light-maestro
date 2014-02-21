#!/usr/bin/env python


import struct


wave_list = []
for s in range(12):
    wave = {'method': 'POST'}
    wave['url'] = 'http://localhost:3520/scenes/{0}/_load'.format(s + 1)
    wave['name'] = 'Scene {0:02}'.format(s + 1)
    wave['data'] = ''
    wave_list.append(wave)


for wave in wave_list:

    req_data = '\n'.join((wave['method'], wave['url'], wave['data']))
    req_len = len(req_data)
    if req_len % 2 == 1:
        req_data += '\n'
        req_len += 1

    file_len = 36 + 8 + req_len

    riff_chunk = struct.pack('<4sL4s', 'RIFF'.encode(), file_len, 'WAVE'.encode())
    fmt_chunk = struct.pack('<4sL2H2L2H', 'fmt '.encode(), 16, 1, 1, 22050, 44100, 2, 16)
    data_chunk = struct.pack('<4sL', 'data'.encode(), 0)
    req_chunk = struct.pack('<4sL', 'req '.encode(), req_len) + req_data.encode()

    with open('../triggers/' + wave['name'] + '.wav', 'wb') as f:
        f.write(riff_chunk + fmt_chunk + data_chunk + req_chunk)
