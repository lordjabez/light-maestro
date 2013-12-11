"""
@copyright: 2013 Single D Software - All Rights Reserved
@summary: Provides the HTTP server for Light Maestro.
"""


# Standard library imports
import collections
import logging
import os
import json
import threading
import time

# Additional library imports
import requests


# Named logger for this module
_logger = logging.getLogger('wavetrigger')

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
    
        # Grab a list of all fully-qualified wave filenames in the trigger folder
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
                method, url, data = req[52:].splitlines()
    
                # Attempt to send the request and log the results    
                _logger.debug('Sending {0} request to {1}'.format(method, url))
                try:
                    response = _session.request(method, url, data=data)
                    _logger.debug('Received response with status code {0}'.format(response.status_code))
                except requests.RequestException:
                    _logger.warning('Unable to contact {0}'.format(url))


def start():
    """Initializes the module."""
    threading.Thread(target=_triggerpoller).start()
