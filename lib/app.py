#!/usr/bin/env python

import asyncio
import json
from websockets.asyncio.server import serve

import logging

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
                    handlers=[stream_handler])




async def handler(websocket):
    print(">> in handler")
    async for message in websocket:
        print(">>> message in handler")
        print(message)
        message_dict = json.loads(message)
        if message_dict["type"] == "play":
            await websocket.send(f'{"play", message_dict["column"]}')

async def main():
    print("> MAIN")
    async with serve(handler, "", 8001) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())