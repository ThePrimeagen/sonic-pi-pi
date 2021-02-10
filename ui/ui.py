import curses
from curses import wrapper
import socket
from functools import reduce
import math
import traceback
import asyncio
from websockets import exceptions as we
import websockets
import os
import logging
import atexit
from tracks import TrackState
from json import dumps, loads

"""
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
"""

def fill_space(track_name: str, length: int) -> str:
    diff = length - len(track_name)
    sep = ' ' if diff > 0 else ''

    return track_name + sep * diff

stdscr = None
async def create_ui_server(websocket, path):
    i = 0
    while True:
        try:
            msg = loads(await websocket.recv())
            print(f"Tracks {msg['tracks']} -- track_names={msg['track_names']}")

            state = TrackState(tracks=msg["tracks"], track_names=msg["track_names"])

            # Clear screen
            stdscr.clear()

            # This raises ZeroDivisionError when i == 10.
            title_length = 20
            content_length = 63
            sep = "|"
            parsed = [
                f"|{'-' * (title_length + 2)}|{'-' * (content_length + 2)}|",
                f"|{' ' * (title_length + 2)}| {'   .   .   .   '.join([str(x) for x in [1, 2, 3, 4, '|']])}"
            ]

            for i in range(0, len(state.tracks)):
                separator = '   ' if len(state.tracks[i]) == 16 else ' '
                tracks = fill_space(separator.join([str(x) for x in state.tracks[i]]), content_length)
                track_name = fill_space(state.track_names[i], title_length)
                parsed.append(f"| {track_name} | {tracks} |")

            for i, out in enumerate(parsed):
                stdscr.addstr(i, 0, out) 

            stdscr.refresh()

        except we.ConnectionClosedError as e:
            return

        except Exception as e:
            print(f"Nice try guy {str(e)}")
            print(traceback.format_exc())


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
