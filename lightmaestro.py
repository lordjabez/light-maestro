#!/usr/bin/env python

"""
@copyright: 2013 Single D Software - All Rights Reserved
@summary: Main module for Light Maestro.
"""


# Standard library imports
import argparse
import logging

# Application imports
import httpserver
import wavetrigger

# Parse the command line parameters
_parser = argparse.ArgumentParser()
_parser.add_argument('-c', '--console', default='GenericConsole', help='console module to use')
_parser.add_argument('-p', '--port', default='/dev/ttyUSB0', help='port on which to communicate')
_parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='enable debug logging')
_args = _parser.parse_args()

# Configure the logging module.
_logformat = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
_loglevel = logging.DEBUG if _args.debug else logging.INFO
logging.basicConfig(format=_logformat, level=_loglevel)

# Initialize the console object depending on command line parameters.
console = __import__(_args.console.lower())
Console = getattr(console, _args.console)
try:
    _console = Console(_args.port)
except TypeError:
    _console = Console()

# Start the application components
httpserver.start(_console)
wavetrigger.start()
