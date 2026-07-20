#!/usr/bin/env python

import asyncio

from websockets.asyncio.server import serve

async def handler(websocket):
    async for message in websocket:
        print(message)

async def main():
    async with serve(handler, "", 8001) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())