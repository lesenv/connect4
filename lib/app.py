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
            event = {"type": "play"}
            pl, col, row = game.moves[-1]
            event["player"] = pl
            event["column"] = col
            event["row"] = row
            await websocket.send(json.dumps(event))
            active_player = change_player[active_player]
        elif message_dict["win"] == "log":
            logger.debug(message_dict["txt"])

async def main():
    logger.debug("> MAIN")
    async with serve(handler, "", 8001) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())