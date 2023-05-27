import argparse

from websockets import connect

import asyncio

parser = argparse.ArgumentParser(description='Connect to websocket')
parser.add_argument(
    'token',
    type=str,
    help='access token',
)


async def listen(token: str):
    async with connect(
        f"ws://localhost:8000/ws/post_request?token={token}"
    ) as websocket:
        await websocket.send("Hello world!")
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")


if __name__ == '__main__':
    args = parser.parse_args()
    asyncio.run(listen(args.token))
