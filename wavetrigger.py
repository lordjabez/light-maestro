"""
@copyright: 2013 Single D Software - All Rights Reserved
@summary: Provides the HTTP server for Light Maestro.
"""


# Standard library imports
import collections
import logging
import os
import threading
import time

# Additional library imports
import requests


# Named logger for this module
_logger = logging.getLogger(__name__)

# Configure requests to not log so much
logging.getLogger('requests.packages.urllib3').setLevel(logging.WARNING)

# We use a session variable so that HTTP keep-alive is utilized, and
# also so we'll always remember to set the content type appropriately.
_session = requests.session()
_session.headers['Content-Type'] = 'application/json'

# Stores previous last access times for each file
# so they can be compared each time files are polled.
_atimes = collections.defaultdict(time.time)


def _triggerpoller():

    # Poll the list of files forever
    while True:

        # Delay the appropriate amount of time between polls
        time.sleep(0.25)

        # Grab a list of all fully-qualified wave file names in the trigger folder
        files = (os.path.join('triggers', f) for f in os.listdir('triggers') if os.path.splitext(f)[1] == '.wav')

        # Iterate over the list of files
        for filename in files:

            # If the last access time is newer than what was previous recorded then take
            # action on that file. A small threshold is used to prevent "double bouncing".
            if os.stat(filename).st_atime - _atimes[filename] > 1.0:

                # Open the file and pull out the data
                with open(filename, 'rb') as f:
                    req = f.read()

                # Immediately store off the last accessed time
                _atimes[filename] = os.stat(filename).st_atime

                # Separate the components of the request
                reqitems = req[52:].splitlines(False)
                method = reqitems[0].decode()
                url = reqitems[1].decode()
                try:
                    data = reqitems[2].decode()
                except IndexError:
                    data = ''

                # Attempt to send the request and log the results
                _logger.debug('Sending {0} request to {1}'.format(method, url))
                try:
                    response = _session.request(method, url, data=data)
                    _logger.debug('Received response with status code {0}'.format(response.status_code))
                except requests.RequestException:
                    _logger.warning('Unable to contact {0}'.format(url))


def writewave(method, url, name, data)

    req_data = '\n'.join((method, url, data))
    req_len = len(req_data)
    if req_len % 2 == 1:
        req_data += '\n'
        req_len += 1

    file_len = 36 + 8 + req_len

    riff_chunk = struct.pack('<4sL4s', 'RIFF'.encode(), file_len, 'WAVE'.encode())
    fmt_chunk = struct.pack('<4sL2H2L2H', 'fmt '.encode(), 16, 1, 1, 22050, 44100, 2, 16)
    data_chunk = struct.pack('<4sL', 'data'.encode(), 0)
    req_chunk = struct.pack('<4sL', 'req '.encode(), req_len) + req_data.encode()

    with open('triggers/' + name + '.wav', 'wb') as f:
        f.write(riff_chunk + fmt_chunk + data_chunk + req_chunk)


def start():
    """Initializes the module."""
    threading.Thread(target=_triggerpoller).start()
