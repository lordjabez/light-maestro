"""
@copyright: 2013 Single D Software - All Rights Reserved
@summary: Provides a console API for Light Maestro.
"""


# Standard library imports
import collections
import json
import logging
import os
import re
import threading
import time


# Named logger for this module
_logger = logging.getLogger(__name__)


# Maximum number of channels supported
maxchannels = 96


class SceneAlreadyChangedError(Exception):
    """Requested scene is changing or already changed."""
    pass


class SceneNotFoundError(Exception):
    """Missing or corrupt scene file."""
    pass


class NotSupportedError(Exception):
    """Console does not support this function."""
    pass


class CommunicationError(Exception):
    """Communication with the console failed."""
    pass


def _alphasort(items):
    """ Sort the given list in the way that humans expect."""
    convert = lambda t: int(t) if t.isdigit() else t
    alphakey = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(items, key=alphakey)


class Console():
    """Abstract class from which all other console classes inherit."""

    def _getscenefilename(self, sceneid):
        return os.path.join(self._scenepath, sceneid)

    def getstatus(self):
        """
        Provide status information for the connection to the console.
        @return: Dictionary containing status information
        """
        status = {'condition': 'operational'}
        status['interface'] = self.__class__.__name__.lower()
        status['fading'] = self._target is not None
        if self._sceneid is not None:
            status['scene'] = self._sceneid
        return status

    def getchannels(self):
        """
        Provide all DMX channel values.
        @return: Dictionary containing all channel numbers and values
        """
        return {'channels': self._channels}

    def loadchannels(self, data, sceneid):
        with self._lock:
            self._target = data.get('channels', {})
            self._fadetime = time.time() + data.get('fade', 0)
            self._sceneid = sceneid

    def getscenes(self):
        try:
            return {'scenes': _alphasort(os.listdir(self._scenepath))}
        except OSError:
            raise CommunicationError

    def getscene(self, sceneid):
        try:
            with open(self._getscenefilename(sceneid)) as f:
                return json.load(f)
        except IOError:
            raise SceneNotFoundError
        except ValueError:
            raise CommunicationError

    def changescene(self, sceneid):
        if self._sceneid == sceneid:
            raise SceneAlreadyChangedError
        scene = self.getscene(sceneid)
        self.loadchannels(scene, sceneid)

    def loadscene(self, sceneid):
        scene = self.getscene(sceneid)
        scene.pop('fade', None)
        self.loadchannels(scene, sceneid)

    def savescene(self, sceneid, fade=5, scene=None):
        if scene is None:
            scene = self.getchannels()
            scene['fade'] = fade
        try:
            with open(self._getscenefilename(sceneid), 'w') as f:
                json.dump(scene, f, indent=4)
        except IOError:
            raise CommunicationError

    def deletescene(self, sceneid):
        try:
            os.remove(self._getscenefilename(sceneid))
        except FileNotFoundError:
            return
        except OSError:
            raise CommunicationError

    def _setchannels(self, channels):
        self._channels.update(channels)

    def _fader(self):
        fadedelay = 0.1
        while True:
            time.sleep(fadedelay)
            if self._target:
                with self._lock:
                    remainingfade = self._fadetime - time.time()
                    if remainingfade > fadedelay:
                        fadechannels = {}
                        for c, v in self._target.items():
                            delta = (self._target[c] - self._channels[c]) * fadedelay / remainingfade
                            fadechannels[c] = self._channels[c] + delta
                        self._setchannels(fadechannels)
                    else:
                        self._setchannels(self._target)
                        self._target = None

    def __init__(self, parameter='scenes'):
        """Initialize the console object."""
        self._channels = collections.OrderedDict((str(c+1), 0.0) for c in range(maxchannels))
        self._target = None
        self._fadetime = time.time()
        self._sceneid = None
        self._lock = threading.Lock()
        self._scenepath = parameter
        try:
            self.changescene('Startup')
        except SceneNotFoundError:
            _logger.warning('Unable to change to startup scene')
        # Start the scene transition task
        threading.Thread(target=self._fader).start()
