import bottle
import json

game = {}

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
    game = data

    return json.dumps({
        'name': 'Dem Franchize Boyz',
        'color': '#00ff00',
        'head_url': 'https://38.media.tumblr.com/tumblr_lzkctzyiTv1qfea58o1_500.gif',
        'taunt': 'My life for Auir!'
    })


@bottle.post('/move')
def move():
    data = bottle.request.json

    return json.dumps({
        'move': move_response(),
        'taunt': 'die!'
    })


@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})

def move_response():
    moves = {'left': test_left,
            'right': test_right,
            'up': test_up,
            'down': test_down
            }
    best_move =  sorted(moves.items(), key = lambda t: t[1], reverse=True)[0][0]
    return best_move


def test_left():
    return 100

def test_right():
    return 0

def test_down():
    return 0

def test_up():
    return 0



# Expose WSGI app
application = bottle.default_app()
