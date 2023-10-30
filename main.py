# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server
    from battlesnake import game
    run_server(game)
