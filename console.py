"""
@copyright: 2013 Single D Software - All Rights Reserved
@summary: Provides a console API for Light Maestro.
"""


# Standard library imports
import logging


# Named logger for this module
_logger = logging.getLogger(__name__)


class CommunicationError(StandardError):
    """Communication with the console failed."""
    pass


def _getlist(nums):
    if type(nums) is str:
        return (int(n) for n in nums.split(','))


class Console:
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
        return {}

    def setcurrentscene(self, scene):
        """
        Set the current scene.
        @param scene: Dictionary containing the scene identifier to make current
        """
        pass
