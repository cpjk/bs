import bottle
import json
import logging
logging.basicConfig(filename='log.txt', format=logging.BASIC_FORMAT)

lean = True
ggame = {}
gsnake_name = 'Dem Franchize Boyz'
gtaunt = ''
gblockers = []
gboard_state = {}
gmults = {
            'wall':0,
            'snake_body':0,
            'food_in_direction': 0.01,
            'bad': 0,
            'close_food': 200
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
        'taunt': 'lean wit it'
    })

def taunt():
    global lean
    lean = not lean
    if lean:
        return 'lean wit it'
    return 'rock wit it'

@bottle.post('/move')
def move():
    global gboard_state
    gboard_state = bottle.request.json

    return json.dumps({
        'move': move_response(),
        'taunt': taunt() 
    })


@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})


def move_response():
    global gboard_state
    board = gboard_state['board']
    snakes = gboard_state['snakes']
    our_snake = find_our_snake(snakes)
    food = order_food(our_snake) 

    moves = { 'left': test_left(board, snakes, food, our_snake),
            'right': test_right(board, snakes, food, our_snake),
            'up': test_up(board, snakes, food, our_snake),
            'down': test_down(board, snakes, food, our_snake) }

    for move in moves:
        print(move, moves[move])
    best_move =  sorted(moves.items(), key = lambda t: t[1], reverse=True)[0][0]
    return best_move


def test_left(board, snakes, food, our_snake):
    global gmults
    our_head = our_snake['coords'][0]
    mult = 1

    left_coords = (our_head[0]-1, our_head[1])

    if our_head[0] == 0:
        mult *= gmults['wall']
    else:
        if is_bad(left_coords, board):
            mult *= gmults['bad']

    #the food in that direction multiplier
    mult *= 1 + gmults['food_in_direction'] * len(food['left'])

    #setup the close food multiplier
    #inverse relationship between the distance to the food
    #and the multiplier
    distance = ggame['width'] if len(food['left']) < 1 else food['left'][0][2]
    
    mult *= (gmults['close_food'] * 1.0) / distance

    return 100 * mult


def test_right(board, snakes, food, our_snake):
    global gmults
    our_head = our_snake['coords'][0]
    mult = 1
    right_coords = (our_head[0]+1, our_head[1])

    if our_head[0] == ggame['width'] - 1:
        mult*=gmults['wall']
    else:
        if is_bad(right_coords, board):
            mult*= gmults['bad']

    # all the food in direction multiplier
    mult *= 1+ gmults['food_in_direction'] * len(food['right'])

    #setup the close food multiplier
    #inverse relationship between the distance to the food
    #and the multiplier
    distance = ggame['width'] if len(food['right']) < 1 else food['right'][0][2]
    mult *= (gmults['close_food']*1.0) /distance
    return 100 * mult


def test_down(board, snakes, food, our_snake):
    global gmults
    our_head = our_snake['coords'][0]
    mult = 1
    down_coords = (our_head[0], our_head[1]+1)

    if our_head[1] == ggame['height'] - 1:
        mult*=gmults['wall']
    else:
        if is_bad(down_coords, board):
            mult*= gmults['bad']

    # if there is a log of food in a particular direction
    #you should want to go in that direction
    mult *= 1 + gmults['food_in_direction'] * len(food['down'])
    
    #setup the close food multiplier
    #inverse relationship between the distance to the food
    #and the multiplier
    distance = ggame['height'] if len(food['down']) < 1 else food['down'][0][2]
    mult *= (gmults['close_food'] *1.0)/distance


    return 100 * mult


def test_up(board, snakes, food, our_snake):
    global gmults
    our_head = our_snake['coords'][0]
    mult = 1
    up_coords = (our_head[0], our_head[1]-1)

    if our_head[1] == 0:
        mult *= gmults['wall']
    else:
        if is_bad(up_coords, board):
            mult*= gmults['bad']

    mult *= 1 + gmults['food_in_direction'] * len(food['up'])

    #setup the close food multiplier
    #inverse relationship between the distance to the food
    #and the multiplier
    distance = ggame['height'] if len(food['up']) < 1 else food['up'][0][2]
    mult *= (gmults['close_food'] *1.0) /distance
    print('this is the multiplier' , mult)

    return 100 * mult


def order_food(our_snake):
    our_head = our_snake['coords'][0]
    ret = { 
            'left': [], 
            'right': [], 
            'up': [], 
            'down': []
          }

    for food in gboard_state['food']:
        #add the food to the food array
        if len(food) < 3:
            food.append(distance(our_head, food))
        if our_head[0] > food[0]:
            ret['left'].append(food) 
        else: 
            ret['right'].append(food) 

        if our_head[1] < food[1]:
            ret['down'].append(food) 
        else: 
            ret['up'].append(food) 

    for direction in ret:
        ret[direction] = sorted(ret[direction], key = lambda x: x[2])
    return ret


def find_our_snake(snakes):
    for snake in snakes:
        if snake['name'] == gsnake_name:
            return snake


def populateBlockers(snakes):
    for snake in snakes:
        for coord in snake["coords"]:
            gblockers.append(coord)


def is_bad(coords, board):
    bad_states = ['head', 'body']
    return board[coords[0]][coords[1]]['state'] in bad_states

def distance(us, them):
    x = us[0] - them[0]
    y = us[1] - them[1]
    return abs(x) + abs(y)

# Expose WSGI app
application = bottle.default_app()
