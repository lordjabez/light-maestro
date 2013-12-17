"""
@copyright: 2013 Single D Software - All Rights Reserved
@summary: Open DMX USB interface for Light Maestro.
"""

# Standard library imports
import logging
import threading
import time

# Additional library imports
import serial

# Application imports
import console


# Named logger for this module
_logger = logging.getLogger(__name__)


class OpenDmxUsb(console.Console):
    """Interface to the Open DMX USB dongle from ENTTEC."""

    def getstatus(self):
        status = super().getstatus()
        status['condition'] = 'operational' if self._portavailable else 'nonoperational'
        status['framecount'] = self._framecount
        status['framerate'] = self._framerate
        return status

    def _setchannels(self, channels):
        super()._setchannels(channels)
        for c, v in self._channels.items():
            self._universe[int(c)] = max(0, min(int(v * 255.0 / 100.0), 255))

    def _dmxwriter(self):
        while True:
            if not self._port.isOpen():
                try:
                    self._port.open()
                except IOError:
                    if self._portavailable:
                        _logger.error('Unable to open port {0}'.format(self._port.name))
                        self._portavailable = False
                    continue
                if not self._portavailable:
                    self._portavailable = True
                    _logger.info('Opened port {0}'.format(self._port.name))
            try:
                self._port.sendBreak(0.001)
                self._port.write(self._universe)
                self._framecount += 1
            except IOError:
                _logger.warning('Could not write to port {0}'.format(self._port.name))
                self._port.close()
                continue

    def _frameratecalculator(self):
        numcounts = 10
        lastframecount = 0
        lastcounts = [0] * numcounts
        slot = 0
        while True:
            lastcounts[slot] = self._framecount - lastframecount
            lastframecount = self._framecount
            slot = (slot + 1) % numcounts
            self._framerate = sum(lastcounts) / float(numcounts)
            time.sleep(1.0)

    def __init__(self, parameter):
        self._universe = bytearray(513)
        self._port = serial.Serial()
        self._port.port = parameter
        self._port.baudrate = 250000
        self._port.stopbits = 2
        self._portavailable = False
        self._framecount = 0
        self._framerate = 0.0
        threading.Thread(target=self._dmxwriter).start()
        threading.Thread(target=self._frameratecalculator).start()
        super().__init__()
