import socket
import asyncio                                    
import websockets                                 
from websockets import exceptions as we
import os
import logging

logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

async def hello(websocket, path):
    print("hello has been called", flush=True)
    while True:
        try:
            print("Awaiting message", flush=True)
            msg = await websocket.recv()
            print(f"> {msg}", flush=True)
            os.system(f"echo \"{msg}\" | sonic_pi")

        except we.ConnectionClosedError as e:
            return

        except Exception as e:
            print(f"Nice try guy {str(e)}")

print("Hello", flush=True)
start_server = websockets.serve(hello, "0.0.0.0", 42069, ping_interval=None)
print("world", flush=True)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

print("fin", flush=True)


