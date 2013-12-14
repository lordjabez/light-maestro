"""
@copyright: 2013 Single D Software - All Rights Reserved
@summary: Elation Magic 260 MIDI interface for Light Maestro.
"""


# Standard library imports
import logging

# Additional library imports
import rtmidi
import rtmidi.midiconstants

# Application imports
import console


# Named logger for this module
_logger = logging.getLogger(__name__)


class ElationMagic(console.Console):
    """The console class that communicates with the Elation Magic 260."""

    def _sendmidi(self, channel, note):
        try:
            self._midi.send_message((rtmidi.midiconstants.NOTE_ON | channel, note, 127))
            _logger.debug('Sent note {0} to channel {1}'.format(note, channel))
        except RuntimeError:
            raise console.CommunicationError

    def getstatus(self):
        """
        Provide status information for the connection to the console.
        @return: Dictionary containing status information
        """
        condition = 'operational' if self._midi else 'nonoperational'
        return {'condition': condition}

    def setcurrentscene(self, scene):
        """
        Set the current scene
        @param scene: Dictionary containing the scene identifier to make current
        """
        channel, note = divmod(int(scene['id']), 72)
        self._sendmidi(channel, note)

    def __init__(self):
        super().__init__()
        self._midi = rtmidi.MidiOut()
        for p, portname in enumerate(self._midi.get_ports()):
            if 'USB' in portname:
                self._midi.open_port(p)
                _logger.info('Connected to MIDI device "{0}"'.format(self._midi.get_port_name(p)))
                return
        _logger.warning('No USB MIDI device found')
