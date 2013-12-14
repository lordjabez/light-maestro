"""
@copyright: 2013 Single D Software - All Rights Reserved
@summary: Provides the HTTP server for Light Maestro.
"""


# Standard library imports
import json
import threading

# Additional library imports
import bottle

# Application imports
import console


# Increase the maximum body size allowed by bottle
bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024

# Regular expressions that define a number and a list of numbers
_numregex = '[0-9]+'
_numsregex = '[0-9]+(,[0-9]+)*'


class _Console(object):
    console = None


@bottle.get('/status')
def _getstatus():
    return _Console.console.getstatus()


@bottle.get('/console')
def _getconsole():
    return _Console.console.getconsole()


@bottle.put('/scenes/_current')
def _putcurrentscene():
    try:
        _Console.console.setcurrentscene(bottle.request.json)
    except console.CommunicationError:
        bottle.abort(503, 'Unable to communicate with console')


@bottle.get('/')
@bottle.get('/<filename:path>')
def _getfile(filename='index.html'):
    return bottle.static_file(filename, root='web')


@bottle.error(404)
@bottle.error(500)
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
    kwargs = {'server': 'rocket', 'host': '0.0.0.0', 'port': 3520, 'debug': False, 'quiet': True}
    threading.Thread(target=bottle.run, kwargs=kwargs).start()
