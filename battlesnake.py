import random
from typing import Dict, List
from scipy import spatial

def info() -> Dict:
    return {
        "apiversion": "1",
        "author": "theCroc itself",
        "color": "#008000",
        "head": "default",
        "tail": "default",
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

def is_move_safe(location: Dict, my_body: List[Dict], my_length:int ,snakes: List[Dict], board_width: int, board_height: int) -> bool:
    if location in my_body:
        return False
    nearby_dangerous_head = False
    for snake in snakes:
        if location in snake["body"]:
            if location == snake['head']:
                if my_length > snake['length']:
                    return True
                return False
            return False
        if spatial.distance.euclidean([location["x"],location["y"]], [snake['head']["x"],snake['head']["y"]]) < 2 and my_length > snake['length']:
            nearby_dangerous_head=True

    if location["x"] < 0 or location["x"] >= board_width or location["y"] < 0 or location["y"] >= board_height or nearby_dangerous_head:
        return False
    return True

def get_safe_moves(possible_moves: Dict, my_body: List[Dict], my_length: int, snakes: List[Dict], board_width: int, board_height: int) -> List[str]:
    return [direction for direction, location in possible_moves.items() if is_move_safe(location, my_body, my_length, snakes, board_width, board_height)]

def get_closest_target(my_head: Dict, targets: List[Dict]) -> Dict:
    targets_distance = [(target, abs(my_head["x"] - target["x"]) + abs(my_head["y"] - target["y"])) for target in targets]
    targets_distance.sort(key=lambda x: x[1])
    return targets_distance[0][0] if targets_distance else None

def move(data: Dict) -> Dict:
    my_head = data["you"]["head"]
    my_body = data["you"]["body"]
    my_length= data["you"]["length"]
    board_width = data["board"]["width"]
    board_height = data["board"]["height"]
    snakes = data["board"]["snakes"]
    foods = data["board"]["food"]

    possible_moves = get_possible_moves(my_head)
    safe_moves = get_safe_moves(possible_moves, my_body, my_length, snakes, board_width, board_height)

    if not safe_moves:
        return {"move": "down"}

    target = get_closest_target(my_head, foods)
    if target:
        moves_to_target = sorted(safe_moves, key=lambda move: spatial.distance.euclidean([possible_moves[move]['x'], possible_moves[move]['y']], [target['x'], target['y']]))
        return {"move": moves_to_target[0]}


    return {"move": random.choice(safe_moves)}

game = {"info": info, "start": start, "move": move, "end": end}
