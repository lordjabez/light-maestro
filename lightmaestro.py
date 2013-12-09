import os
import time

try:
    from simplecoremidi import send_midi
except ImportError:
    def send_midi(command, note, velocity):
        print 'DEBUG:', command, note, velocity

_folder = 'Scenes'
_polldelay = 0.25

_starttime = time.time()

_atimes = {}

while True:
    time.sleep(_polldelay)
    for f in os.listdir(_folder):
        fpath = os.path.join(_folder, f)
        atime = os.stat(fpath).st_atime
        lastatime = _atimes.get(f, _starttime)
        if atime - lastatime > 1.0:
            _atimes[f] = atime
            _, p, _, s = os.path.splitext(f)[0].split()
            i = (int(p) - 1) * 24 + int(s) - 1
            channel, note = divmod(i, 72)
            send_midi(0x90 | channel, note, 127)
            time.sleep(_polldelay)
            send_midi(0x90 | channel, note, 0)  # TODO is the note-off command necessary?
