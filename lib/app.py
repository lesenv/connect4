#!/usr/bin/env python
import asyncio
import json
from itertools import cycle as iter_cycle

from websockets.asyncio.server import serve
from connect4 import Connect4, PLAYER1, PLAYER2

import logging
logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler()
# when needed, back to DEBUG (change from INFO)
stream_handler.setLevel(logging.INFO)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
                    handlers=[stream_handler])

async def handler(websocket):
    logger.debug(">> in handler")
    # new Game-instance of Connect4
    game = Connect4()
    # gather the players
    players = iter_cycle([PLAYER1, PLAYER2])
    active_player = next(players)

    async for message in websocket:
        logger.debug(f"\n>>> message in handler")
        logger.debug(message)
        message_dict = json.loads(message)
        if message_dict["type"] == "play":
            try:
                game.play(active_player, message_dict["column"])
            except ValueError as e:
                event_error = {
                    "type": "error",
                    "message": str(e)
                }
                await websocket.send(json.dumps(event_error))
                continue

            pl, col, row = game.moves[-1]
            event = {
                "type": "play",
                "player": pl,
                "column": col,
                "row": row
                }
            await websocket.send(json.dumps(event))
            if game.winner:
                event_won = {
                    "type": "win",
                    "player": game.winner
                }
                await websocket.send(json.dumps(event_won))
            active_player = next(players)
        elif message_dict["win"] == "log":
            logger.info(message_dict["txt"])

async def main():
    logger.debug("> MAIN")
    async with serve(handler, "", 8001) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())