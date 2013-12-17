"""
@copyright: 2013 Single D Software - All Rights Reserved
@summary: Provides a console API for Light Maestro.
"""


# Standard library imports
import collections
import json
import logging


# Named logger for this module
_logger = logging.getLogger(__name__)


class SceneNotFoundError(Exception):
    """Missing or corrupt scene file."""
    pass


class CommunicationError(Exception):
    """Communication with the console failed."""
    pass


class Console():
    """Abstract class from which all other console classes inherit."""

    def getstatus(self):
        """
        Provide status information for the connection to the console.
        @return: Dictionary containing status information
        """
        return {'module': self.__class__.__name__.lower(), 'condition': 'operational'}

    def getchannels(self):
        """
        Provide all DMX channel values.
        @return: Dictionary containing all channel numbers and values
        """
        return self._channels

    def setchannels(self, channels):
        """
        Set a collection of channels to particular values
        @param channels: Dictionary containing the channel numbers and values to update
        """
        self._channels.update(channels)

    def loadscene(self, sceneid):
        """
        Set the current scene.
        @param scene: Dictionary containing the scene identifier to make current
        """
        scenefile = 'scenes/{0}.json'.format(sceneid)
        try:
            with open(scenefile) as f:
                scene = json.load(f)
        except (IOError, ValueError):
            raise SceneNotFoundError
        self.setchannels(scene.get('channels', {}))
        _logger.debug('Loading scene {0}'.format(sceneid))

    def __init__(self, parameter=None):
        """Initialize the console object."""
        # Set up the channel value dictionary.
        self._channels = collections.OrderedDict((str(c+1), 0) for c in range(512))
        # Load scene 0 by default.
        try:
            self.loadscene(0)
        except SceneNotFoundError:
            _logger.warning('Unable to load default scene, all channels set to zero')
