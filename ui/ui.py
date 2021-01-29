import curses
from curses import wrapper
import socket
import asyncio                                    
from websockets import exceptions as we
import websockets
import os
import logging
import atexit

"""
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
"""

stdscr = None

async def create_ui_server(websocket, path):
    print("Got websocket");
    i = 0
    while True:
        try:
            print("awaiting message");
            msg = await websocket.recv()
            print("got message", msg);

            # Clear screen
            stdscr.clear()

            # This raises ZeroDivisionError when i == 10.
            stdscr.addstr(i % 10, 0, f"{i}: {msg}")
            i += 1

            stdscr.refresh()

        except we.ConnectionClosedError as e:
            return

        except Exception as e:
            print(f"Nice try guy {str(e)}")

stdscr = curses.initscr()
def on_end():
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

atexit.register(on_end)

curses.noecho()
curses.cbreak()
stdscr.keypad(True)

start_server = websockets.serve(create_ui_server, "0.0.0.0", 6969, ping_interval=None)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
