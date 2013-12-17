"""
@copyright: 2013 Single D Software - All Rights Reserved
@summary: Debugging console interface for Light Maestro.
"""

# Standard library imports
import logging
import threading
import time

# Application imports
import console


# Named logger for this module
_logger = logging.getLogger(__name__)


class LoggingConsole(console.Console):
    """Provide a generic console class that's useful for deubgging."""

    def _channellogger(self):
        while True:
            time.sleep(self._polldelay)
            values = (int(v) for c, v in self._channels.items() if int(c) <= self._maxchannels)
            valuesstr = ' '.join('{0:03}'.format(v) for v in values)
            _logger.info(valuesstr)

    def __init__(self, parameter):
        params = parameter.split(',')
        self._maxchannels = int(params[0])
        self._polldelay = 1.0 / float(params[1])
        super().__init__()
        threading.Thread(target=self._channellogger).start()
