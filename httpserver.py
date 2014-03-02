"""
@copyright: 2013 Single D Software - All Rights Reserved
@summary: Provides the HTTP server for Light Maestro.
"""


# Standard library imports
import json
import logging
import threading

# Additional library imports
import bottle

# Application imports
import console


# TODO: add JSON validation

class _Console(object):
    console = None


@bottle.get('/status')
def _getstatus():
    return {'status': _Console.console.getstatus()}


@bottle.get('/channels')
def _getchannels():
    try:
        return {'channels': _Console.console.getchannels()}
    except console.NotSupportedError:
        bottle.abort(501, 'Console does not support this function')
    except console.CommunicationError:
        bottle.abort(503, 'Unable to communicate with console')


@bottle.post('/channels/_load')
def _postchannelsload():
    try:
        _Console.console.loadchannels(bottle.request.json)
        bottle.response.status = 202
    except console.NotSupportedError:
        bottle.abort(501, 'Console does not support this function')
    except console.CommunicationError:
        bottle.abort(503, 'Unable to communicate with console')


@bottle.get('/scenes')
def _getscenes():
    try:
        return {'scenes': _Console.console.getscenes()}
    except console.NotSupportedError:
        bottle.abort(501, 'Console does not support this function')
    except console.CommunicationError:
        bottle.abort(503, 'Unable to communicate with console')


@bottle.get('/scenes/<sceneid>')
def _getscene(sceneid):
    try:
        return _Console.console.getscene(sceneid)
    except console.SceneNotFoundError:
        bottle.abort(404, 'Scene "{0}" not found'.format(sceneid))
    except console.NotSupportedError:
        bottle.abort(501, 'Console does not support this function')
    except console.CommunicationError:
        bottle.abort(503, 'Unable to communicate with console')


@bottle.put('/scenes/<sceneid>')
def _putscene(sceneid):
    try:
        _Console.console.savescene(sceneid, bottle.request.json)
    except console.NotSupportedError:
        bottle.abort(501, 'Console does not support this function')
    except console.CommunicationError:
        bottle.abort(503, 'Unable to communicate with console')


@bottle.delete('/scenes/<sceneid>')
def _deletescene(sceneid):
    try:
        _Console.console.deletescene(sceneid)
    except console.NotSupportedError:
        bottle.abort(501, 'Console does not support this function')
    except console.CommunicationError:
        bottle.abort(503, 'Unable to communicate with console')


@bottle.post('/scenes/<sceneid>/_change')
def _postscenechange(sceneid):
    try:
        _Console.console.changescene(sceneid)
        bottle.response.status = 202
    except console.SceneAlreadyChangedError:
        bottle.response.status = 200
    except console.SceneNotFoundError:
        bottle.abort(404, 'Scene "{0}" not found'.format(sceneid))
    except console.NotSupportedError:
        bottle.abort(501, 'Console does not support this function')
    except console.CommunicationError:
        bottle.abort(503, 'Unable to communicate with console')


@bottle.post('/scenes/<sceneid>/_load')
def _postsceneload(sceneid):
    try:
        _Console.console.loadscene(sceneid)
        bottle.response.status = 200
    except console.SceneNotFoundError:
        bottle.abort(404, 'Scene "{0}" not found'.format(sceneid))
    except console.NotSupportedError:
        bottle.abort(501, 'Console does not support this function')
    except console.CommunicationError:
        bottle.abort(503, 'Unable to communicate with console')


@bottle.post('/scenes/<sceneid>/_save')
def _postscenesave(sceneid):
    try:
        _Console.console.savescene(sceneid)
    except console.NotSupportedError:
        bottle.abort(501, 'Console does not support this function')
    except console.CommunicationError:
        bottle.abort(503, 'Unable to communicate with console')


@bottle.get('/data')
def _getdata():
    try:
        status = _Console.console.getstatus()
        channels = _Console.console.getchannels()
        scenes = _Console.console.getscenes()
        return {'status': status, 'channels': channels, 'scenes': scenes}
    except console.NotSupportedError:
        bottle.abort(501, 'Console does not support this function')
    except console.CommunicationError:
        bottle.abort(503, 'Unable to communicate with console')


@bottle.get('/')
@bottle.get('/<filename:path>')
def _getfile(filename='scenes.html'):
    return bottle.static_file(filename, root='web')


@bottle.error(404)
@bottle.error(500)
@bottle.error(501)
@bottle.error(503)
def _returnerror(error):
    """
    Return a custom error message for invalid or failed requests.
    @param error: HTTPError object (hopefully) describing what went wrong.
    """
    # For some reason bottle doesn't automatically convert dicts
    # to JSON in the error handler, so we have to do it manually.
    bottle.response.content_type = 'application/json'
    return json.dumps({'error': error.body})


def start(con):
    """Initializes the module.
    @param con: The console object into which the interface functions will call.
    """
    _Console.console = con
    kwargs = {'host': '0.0.0.0', 'port': 3520, 'debug': False, 'quiet': True}
    threading.Thread(target=bottle.run, kwargs=kwargs).start()

