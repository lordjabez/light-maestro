import midi

for c in range(16):
    for p in range(72):
        tracks = midi.Track()
        tracks.append([])
        tracks[0].append(midi.NoteOnEvent(tick=0, channel=c, pitch=p, velocity=127))
        tracks[0].append(midi.NoteOnEvent(tick=500, channel=c, pitch=p, velocity=0))
        tracks[0].append(midi.EndOfTrackEvent(tick=1000))
        pattern = midi.Pattern(tracks=tracks, resolution=1000, format=0)
        page = ((c * 3) + p // 24) + 1
        scene = (p % 24) + 1
        midi.write_midifile('Scenes/Page {0:02} Scene {1:02}.mid'.format(page, scene), pattern)
