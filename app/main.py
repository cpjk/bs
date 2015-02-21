import bottle
import json
import logging
logging.basicConfig(filename='log.txt', format=logging.BASIC_FORMAT)

ggame = {}
gsnake_name = 'Dem Franchize Boyz'
gtaunt = ''
gboard_state = {}
mults = {
            'wall':0,
            'snake_body':0
        }

@bottle.get('/')
def index():
    return """
        <a href="https://github.com/sendwithus/battlesnake-python">
            battlesnake-python
        </a>
    """


@bottle.post('/start')
def start():
    global ggame
    data = bottle.request.json
    ggame = data

    return json.dumps({
        'name': gsnake_name,
        'color': '#00ff00',
        'head_url': 'https://38.media.tumblr.com/tumblr_lzkctzyiTv1qfea58o1_500.gif',
        'taunt': 'My life for Auir!'
    })


@bottle.post('/move')
def move():
    global gboard_state
    gboard_state = bottle.request.json
    logging.error(gboard_state['board'][0])
    logging.error('\n\n\n')

    return json.dumps({
        'move': move_response(),
        'taunt': move_response()
    })


@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})

def move_response():
    global gboard_state
    board = gboard_state['board']
    snakes = gboard_state['snakes']
    food = gboard_state['food']
    our_snake = find_our_snake(snakes)

    moves = { 'left': test_left(board, snakes, food, our_snake),
            'right': test_right(board, snakes, food, our_snake),
            'up': test_up(board, snakes, food, our_snake),
            'down': test_down(board, snakes, food, our_snake) }

    best_move =  sorted(moves.items(), key = lambda t: t[1], reverse=True)[0][0]

    return best_move


def test_left(board, snakes, food, our_snake):
    our_head = our_snake['coords'][0]
    print(our_head)
    mult = 1

    if our_head[0] == 0:
        mult*=mults['wall']
    # is there a snake ther
    return 100 * mult

def test_right(board, snakes, food, our_snake):
    our_head = our_snake['coords'][0]
    mult = 1
    if our_head[0] == ggame['width'] - 1:
        mult*=mults['wall']
    return 100 * mult 

def test_down(board, snakes, food, our_snake):
    our_head = our_snake['coords'][0]
    mult = 1
    if our_head[1] == ggame['height'] - 1:
        mult*=mults['wall']
    return 100 * mult

def test_up(board, snakes, food, our_snake):
    our_head = our_snake['coords'][0]
    mult = 1
    if our_head[1] == 0:
        mult *= mults['wall']
    return 100 * mult 

def find_our_snake(snakes):
    for snake in snakes:
        if snake['name'] == gsnake_name:
            return snake

# Expose WSGI app
application = bottle.default_app()
