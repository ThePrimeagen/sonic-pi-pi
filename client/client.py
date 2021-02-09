import socket
import asyncio
import websockets
import curses
from twitch import create_twitch_connection, is_command_msg
from utils import MUSIC_SERVER, UI_SERVER
from tracks import TrackList, TrackState
from json import dumps, loads
from dataclasses import asdict


async def create_websocket(server):
    uri = f"ws://{server}"
    return await websockets.connect(uri, ping_interval=None)


def log(string):
    print(string, flush=True)


# First ever beat
"""
track_names = [
    ":drum_cymbal_closed",
    ":drum_bass_soft",
    ":drum_snare_soft",
]
tracks = [
    [5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0],
    [5,0,0,5,5,5,0,0,5,5,5,5,0,0,0,0],
    [0,5,5,0,5,0,5,0,5,5,5,0,0,0,0,5],
]
"""

def string_state(state: TrackState) -> str: 
    return dumps(asdict(state))

async def run_bot(twitch):
    music_server = await create_websocket(MUSIC_SERVER)
    ui_server = await create_websocket(UI_SERVER)
    track_list = TrackList()

    # clear previous state
    await music_server.send(track_list.get_music())
    await ui_server.send(string_state(track_list.get_state()))

    while True:
        # TODO: Make this async generator...
        user, msg = next(twitch)
        if user is not None and is_command_msg(msg):
            print("Got twitch message", msg, "from", user, flush=True)
            if track_list.run_command(user, msg):
                await music_server.send(track_list.get_music())
                await ui_server.send(string_state(track_list.get_state()))

async def main():
    twitch = create_twitch_connection()
    await run_bot(twitch())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
