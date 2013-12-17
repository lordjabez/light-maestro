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


DMX_HEADER = '\x7e\x06\x00\x02'.encode()
DMX_FOOTER = '\xe7'.encode()

class DmxUsbPro(console.Console):
    """Interface to ENTTEC DMX USB Pro compatible devices."""

    def getstatus(self):
        status = super().getstatus()
        status['condition'] = 'operational' if self._portavailable else 'nonoperational'
        return status

    def _setchannels(self, channels):
        super()._setchannels(channels)
        for c, v in self._channels.items():
            self._universe[int(c)] = max(0, min(int(v * 255.0 / 100.0), 255))
        if not self._port.isOpen():
            try:
                self._port.open()
            except IOError:
                if self._portavailable:
                    _logger.error('Unable to open port {0}'.format(self._port.name))
                    self._portavailable = False
                return
            if not self._portavailable:
                self._portavailable = True
                _logger.info('Opened port {0}'.format(self._port.name))
        try:
            self._port.write(DMX_HEADER + bytes(self._universe[1:]) + DMX_FOOTER)
        except IOError:
            _logger.warning('Could not write to port {0}'.format(self._port.name))
            self._port.close()
            return

    def __init__(self, parameter):
        self._universe = bytearray(513)
        self._port = serial.Serial()
        self._baudrate = 115200
        self._port.port = parameter
        self._portavailable = False
        super().__init__()
