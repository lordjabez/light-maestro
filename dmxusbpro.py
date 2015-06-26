"""
@copyright: 2013 Single D Software - All Rights Reserved
@summary: DMX USB Pro interface for Light Maestro.
"""

# Standard library imports
import logging

# Additional library imports
import serial

# Application imports
import console


# Named logger for this module
_logger = logging.getLogger(__name__)


_dmxheader = bytearray([0x7e, 0x06])
_dmxfooter = bytearray([0xe7])


class DmxUsbPro(console.Console):
    """Interface to ENTTEC DMX USB Pro compatible devices."""

    def _openport(self):
        if not self._port.isOpen():
            try:
                self._port.open()
            except IOError:
                if self._portavailable or self._portavailable is None:
                    _logger.error('Unable to open port {0}'.format(self._port.name))
                    self._portavailable = False
                return
            if not self._portavailable:
                self._portavailable = True
                _logger.info('Opened port {0}'.format(self._port.name))

    def _closeport(self):
        self._port.close()

    def getstatus(self):
        status = super().getstatus()
        status['condition'] = 'operational' if self._portavailable else 'nonoperational'
        return status

    def _setchannels(self, channels):
        super()._setchannels(channels)
        for c, v in self._channels.items():
            value = max(0, min(int(v * 255.0 / 100.0), 255))
            try:
                self._universe[int(c)] = value
            except IndexError:
                _logger.warning('Ignoring channel {0} since universe max is {1}'.format(c, console.maxchannels))
        self._openport()
        try:
            self._port.write(_dmxheader + self._dmxsize + self._universe + _dmxfooter)
        except IOError:
            _logger.warning('Could not write to port {0}'.format(self._port.name))
            self._closeport()

    def __init__(self, parameter):
        self._universe = bytearray(console.maxchannels + 1)
        self._dmxsize = bytearray(reversed(divmod(len(self._universe), 256)))
        self._port = serial.Serial()
        self._baudrate = 115200
        self._port.port = parameter
        self._portavailable = None
        super().__init__()
