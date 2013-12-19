#!/usr/bin/env python

# Standard library imports
import argparse
import collections
import logging
import os
import time

# Additional library imports
import requests


# Named logger for this module
_logger = logging.getLogger(__name__)

# Parse the command line arguments
_parser = argparse.ArgumentParser('')
_parser.add_argument('-t', '--triggers', default='triggers', help='Folder containing trigger files')
_parser.add_argument('-r', '--rate', default=4.0, help='Poll rate in polls per second')
_parser.add_argument('-d', '--debug', action='store_true', help='Enables debug logging')
_args = _parser.parse_args()

# Configure the logging module
_logformat = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
_loglevel = logging.DEBUG if _args.debug else logging.INFO
logging.basicConfig(format=_logformat, level=_loglevel)
logging.getLogger('requests.packages.urllib3').setLevel(logging.WARNING)

# We use a session variable so that HTTP keep-alive is utilized, and
# also so we'll always remember to set the content type appropriately.
_session = requests.session()
_session.headers['Content-Type'] = 'application/json'

# Stores previous last access times for each file
# so they can be compared each time files are polled.
_atimes = collections.defaultdict(time.time)


# Poll the list of files forever
while True:

    # Delay the appropriate amount of time between polls
    time.sleep(1.0 / _args.rate)

    # Grab a list of all fully-qualified wave file names in the trigger folder
    files = (os.path.join(_args.triggers, f) for f in os.listdir(_args.triggers) if os.path.splitext(f)[1] == '.wav')

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
            method, url, data = req[52:].splitlines(False)

            # Attempt to send the request and log the results
            _logger.debug('Sending {0} request to {1}'.format(method, url))
            try:
                response = _session.request(method, url, data=data)
                _logger.debug('Received response with status code {0}'.format(response.status_code))
            except requests.RequestException:
                _logger.warning('Unable to contact {0}'.format(url))
