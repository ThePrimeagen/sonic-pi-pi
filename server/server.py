import socket
import asyncio
import websockets
import os

async def hello(websocket, path):
    while True:
        try:
            msg = await websocket.recv()
            print(f"> {msg}", flush=True)
            os.system(f"echo \"{msg}\" | sonic_pi")
        except Exception as e:
            print(f"Exception raised {str(e)}")
            return

start_server = websockets.serve(hello, "0.0.0.0", 42069)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

