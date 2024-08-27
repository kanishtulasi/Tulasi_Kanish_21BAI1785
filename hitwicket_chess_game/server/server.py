# server/server.py

import asyncio
import websockets
import json
from game_logic import update_game_state

GRID_SIZE = 5

async def handle_client(websocket, path):
    print("Client connected")  # Log when a client connects
    
    # Initialize the game
    board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    players = {
        'A': {'pieces': ['P1', 'P2', 'H1', 'H2'], 'row': 0},
        'B': {'pieces': ['P1', 'P2', 'H1', 'H2'], 'row': GRID_SIZE - 1}
    }
    current_turn = 'A'  # Initial turn
    
    while True:
        try:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Received message: {data}")  # Log received messages

            if data['type'] == 'init':
                # Send the initial game state
                await notify_state_update(websocket, board, players, current_turn)

            elif data['type'] == 'move':
                player = data['player']
                move = data['move']
                board, players, valid = update_game_state(board, players, move, player)
                if valid:
                    current_turn = 'B' if current_turn == 'A' else 'A'
                    await notify_state_update(websocket, board, players, current_turn)
                else:
                    await websocket.send(json.dumps({'type': 'invalid_move'}))
        except websockets.ConnectionClosed:
            print("Client disconnected")
            break

async def notify_state_update(websocket, board, players, current_turn):
    game_state = {
        'type': 'state_update',
        'board': board,
        'currentTurn': current_turn
    }
    await websocket.send(json.dumps(game_state))

async def main():
    async with websockets.serve(handle_client, "localhost", 8766):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
