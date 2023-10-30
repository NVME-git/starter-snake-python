# TODO: Define risky moves as backups if no safe moves
# TODO: Avoid loops
# TODO: Rank moves and choose best move

import random
from typing import Dict, List
from scipy import spatial
import logging
logging.basicConfig(level='DEBUG')
'''
Logging Level: When it’s used

DEBUG: Detailed information, typically of interest only when diagnosing problems.

INFO: Confirmation that things are working as expected.

WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.

ERROR: Due to a more serious problem, the software has not been able to perform some function.

CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
'''

def info() -> Dict:
    return {
        "apiversion": "1",
        "author": "Atiyyah Limalia",
        "color": "#40E0D0",
        "head": "do-sammy",
        "tail": "round-bum",
    }

def start(game_state: Dict):
    print("GAME START")

def end(game_state: Dict):
    print("GAME OVER\n")

def get_possible_moves(my_head: Dict) -> Dict:
    return {
        "up": {"x": my_head["x"], "y": my_head["y"] + 1},
        "down": {"x": my_head["x"], "y": my_head["y"] - 1},
        "left": {"x": my_head["x"] - 1, "y": my_head["y"]},
        "right": {"x": my_head["x"] + 1, "y": my_head["y"]}
    }

def is_move_safe(direction:str, location: Dict, my_id:str, my_body: List[Dict], my_length:int ,snakes: List[Dict], board_width: int, board_height: int) -> bool:
    logging.debug(f"direction: {direction}")
    if location in my_body:
        logging.debug(f"{direction}: adjacent my body -> {False}")
        return False
    nearby_dangerous_snake_head = False
    for snake in snakes:
        snake_name = snake['name']
        if my_id == snake['id']:
            logging.debug(f"ignoring my snake's name: {snake_name}")
            continue 
        logging.debug(f"snake's name: {snake_name}")
        if location in snake["body"]:
            if location == snake['head']:
                if my_length > snake['length']:
                    logging.debug(f"{direction}: adjacent shorter snake's head -> {True}")
                    return True
                logging.debug(f"{direction}: adjacent longer snake's head -> {False}")
                return False
            logging.debug(f"{direction}: adjacent snake's body -> {False}")
            return False
        nearby_head = spatial.distance.euclidean([location["x"],location["y"]], [snake['head']["x"],snake['head']["y"]]) <= 2 
        dangerous_snake = my_length <= snake['length']
        logging.debug(f"nearby head: {nearby_head}, dangerous snake: {dangerous_snake}")
        if nearby_head and dangerous_snake:
            nearby_dangerous_snake_head=True
            logging.debug(f"nearby dangerous snake head: {snake_name} -> {nearby_dangerous_snake_head}")

    if location["x"] < 0 or location["x"] >= board_width or location["y"] < 0 or location["y"] >= board_height or nearby_dangerous_snake_head:
        logging.debug(f"{direction}: adjacent boundary or nearby longer snake's head -> {False}")
        return False
    return True

def get_safe_moves(possible_moves: Dict, my_id:str, my_body: List[Dict], my_length: int, snakes: List[Dict], board_width: int, board_height: int) -> List[str]:
    return [direction for direction, location in possible_moves.items() if is_move_safe(direction, location, my_id, my_body, my_length, snakes, board_width, board_height)]

def get_closest_target(my_head: Dict, targets: List[Dict]) -> Dict:
    targets_distance = [(target, abs(my_head["x"] - target["x"]) + abs(my_head["y"] - target["y"])) for target in targets]
    targets_distance.sort(key=lambda x: x[1])
    return targets_distance[0][0] if targets_distance else None

def avoid_hazards(hazards:List[Dict], safe_moves: List[str], possible_moves:Dict) -> List[str]:
    logging.debug(f"hazards:{hazards}")
    new_safe_moves = []
    for safe_move in safe_moves:
        safe_coord = possible_moves[safe_move]
        if safe_coord in hazards: # add hazardous move to the end of the list
            new_safe_moves = new_safe_moves + [safe_move]
        else: # add safe move to the front of the list
            new_safe_moves = [safe_move] + new_safe_moves
    logging.debug(f"new safe moves:{new_safe_moves}")
    return new_safe_moves


def move(data: Dict) -> Dict:
    turn_number = data['turn']
    logging.debug(f'Turn: {turn_number}')
    my_head = data["you"]["head"]
    my_body = data["you"]["body"]
    my_length= data["you"]["length"]
    my_id= data["you"]["id"]
    board_width = data["board"]["width"]
    board_height = data["board"]["height"]
    snakes = data["board"]["snakes"]
    foods = data["board"]["food"]
    hazards = data["board"]["hazards"]

    possible_moves = get_possible_moves(my_head)
    safe_moves = get_safe_moves(possible_moves, my_id, my_body, my_length, snakes, board_width, board_height)
    logging.debug(f'safe moves: {safe_moves}')

    if not safe_moves:
        logging.debug(f'Turn {turn_number} default move played: {True}')
        return {"move": "down"}

    safe_moves = avoid_hazards(hazards, safe_moves, possible_moves)
    target = get_closest_target(my_head, foods)
    if target:
        safe_moves = sorted(safe_moves, key=lambda move: spatial.distance.euclidean([possible_moves[move]['x'], possible_moves[move]['y']], [target['x'], target['y']]))
        logging.debug(f'sorted safe moves by targets: {safe_moves}')
        chosen_move = safe_moves[0]
        logging.debug(f'Turn {turn_number} target chosen move: {chosen_move}')
        return {"move": chosen_move}


    chosen_move = random.choice(safe_moves)
    logging.info(f'Turn {turn_number} chosen move: {chosen_move}')
    return {"move": chosen_move}

game = {"info": info, "start": start, "move": move, "end": end}
