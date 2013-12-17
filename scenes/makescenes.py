import collections
import json


channels = collections.OrderedDict((str(c+1), 255) for c in range(12))
with open('0.json', 'wb') as f:
    json.dump({'channels': channels, 'fade': 0.0}, f, indent=4)


for i in range(12):
    channels = collections.OrderedDict((str(c+1), 0) for c in range(12))
    channels[str(i+1)] = 255
    with open(str(i+1) + '.json', 'wb') as f:
        json.dump({'channels': channels, 'fade': 5.0}, f, indent=4)
