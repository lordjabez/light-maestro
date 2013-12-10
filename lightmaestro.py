#!/usr/bin/env python

import os
import time

import rtmidi

_folder = 'triggers'
_polldelay = 0.25

_starttime = time.time()

_atimes = {}

midi = rtmidi.MidiOut()
usbports = [p for p in midi.get_ports() if 'USB' in p]

if not usbports:
    print('No USB MIDI adapter found.')
    exit(1)

midi.open_port(name=usbports[0])

while True:
    time.sleep(_polldelay)
    for f in os.listdir(_folder):
        fpath = os.path.join(_folder, f)
        atime = os.stat(fpath).st_atime
        lastatime = _atimes.get(f, _starttime)
        print(f, lastatime, atime)
        if atime - lastatime > 1.0:
            _atimes[f] = atime
            _, p, _, s = os.path.splitext(f)[0].split()
            i = (int(p) - 1) * 24 + int(s) - 1
            channel, note = divmod(i, 72)
            midi.send_message((0x90 | channel, note, 127))
            print('Sent note {0} to channel {1}'.format(note, channel))
