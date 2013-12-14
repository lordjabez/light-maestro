"""
@copyright: 2013 Single D Software - All Rights Reserved
@summary: Provides a console API for Light Maestro.
"""


# Standard library imports
import logging


# Named logger for this module
_logger = logging.getLogger(__name__)


class CommunicationError(Exception):
    """Communication with the console failed."""
    pass


def _getlist(nums):
    if type(nums) is str:
        return (int(n) for n in nums.split(','))


class Console():
    """Abstract class from which all other console classes inherit."""

    def getstatus(self):
        """
        Provide status information for the connection to the console.
        @return: Dictionary containing status information
        """
        return {'condition': 'operational'}

    def getconsole(self):
        """
        Provide all console values.
        @return: Dictionary containing the entire console structure
        """
        return {'show': self._show, 'scene': self._scene}

    def setcurrentshow(self, show):
        """
        Set the current show.
        @param show: Dictionary containing the show identifier to make current
        """
        self._show = show

    def setcurrentscene(self, scene):
        """
        Set the current scene.
        @param scene: Dictionary containing the scene identifier to make current
        """
        self._scene = scene

    def __init__(self):
        self._show = None
        self._scene = None
