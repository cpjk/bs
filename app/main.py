import bottle
import json


@bottle.get('/')
def index():
    return """
        <a href="https://github.com/sendwithus/battlesnake-python">
            battlesnake-python
        </a>
    """


@bottle.post('/start')
def start():
    data = bottle.request.json

    return json.dumps({
        'name': 'Dem Franchize Boyz',
        'color': '#00ff00',
        'head_url': 'https://glacial-escarpment-3430.herokuapp.com/',
        'taunt': 'My life for Auir!'
    })


@bottle.post('/move')
def move():
    data = bottle.request.json

    return json.dumps({
        'move': 'left',
        'taunt': ''
    })


@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})

def move_response
    pass

# Expose WSGI app
application = bottle.default_app()
