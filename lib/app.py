#!/usr/bin/env python

import asyncio
import json
from websockets.asyncio.server import serve
from connect4 import Connect4, PLAYER1, PLAYER2

import logging
logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
                    handlers=[stream_handler])




async def handler(websocket):
    logger.debug(">> in handler")
    game = Connect4()
    active_player = PLAYER1
    change_player = {
        PLAYER1: PLAYER2,
        PLAYER2: PLAYER1
    }

    async for message in websocket:
        logger.debug(f"\n>>> message in handler")
        logger.debug(message)
        message_dict = json.loads(message)
        if message_dict["type"] == "play":
            game.play(active_player, message_dict["column"])
            pl, col, row = game.moves[-1]
            event = {
                "type": "play",
                "player": pl,
                "column": col,
                "row": row
                }
            try:
                await websocket.send(json.dumps(event))
            except ValueError as e:
                event_error = {
                    "type": "error",
                    "msg": e
                }
                await websocket.send(json.dumps(event_error))
            if game.winner:
                event_won = {
                    "type": "win",
                    "player": game.winner
                }
                await websocket.send(json.dumps(event_won))
            active_player = change_player[active_player]
        elif message_dict["win"] == "log":
            logger.info(message_dict["txt"])

async def main():
    logger.debug("> MAIN")
    async with serve(handler, "", 8001) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())