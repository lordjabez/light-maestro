import collections
import json


channels = collections.OrderedDict((str(c+1), 100.0) for c in range(12))
with open('../scenes/Default', 'wb') as f:
    json.dump({'channels': channels, 'fade': 0.0}, f, indent=4)


for i in range(12):
    channels = collections.OrderedDict((str(c+1), 0) for c in range(12))
    channels[str(i+1)] = 100.0
    with open('../scenes/' + str(i+1), 'wb') as f:
        json.dump({'channels': channels, 'fade': 5.0}, f, indent=4)
