import socket
import asyncio
import websockets
import curses
from twitch import create_twitch_connection
from utils import MUSIC_SERVER, UI_SERVER

async def create_websocket(server):
    uri = f"ws://{server}"
    return await websockets.connect(uri, ping_interval=None)

def log(string):
    print(string, flush=True)

def create_track_positions():
    return [
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0
    ]

tracks = [
    create_track_positions(),
    create_track_positions(),
    create_track_positions(),
]

# First ever beat
"""
tracks = [
    [5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0],
    [5,0,0,5,5,5,0,0,5,5,5,5,0,0,0,0],
    [0,5,5,0,5,0,5,0,5,5,5,0,0,0,0,5],
]
"""

track_names = [
    ":drum_cymbal_closed",
    ":drum_bass_soft",
    ":drum_snare_soft",
]

def get_state():
    return "hello, world"

def get_music():
    content = f"""
use_bpm 120

        """
    for i, x in enumerate(tracks):
        content += f"""
track{i} = [{",".join(list(map(str, x)))}]
track{i}_name = {track_names[i]}
"""

    content += """
live_loop :pulse do
    sleep 4
end

define :run_p do |name, pattern, sample_name|
    sync :pulse
    live_loop name do
        pattern.each do |p|
            sample sample_name, amp: p/9.0
            sleep 0.25
        end
    end
end
"""
    for i, x in enumerate(tracks):
        content += f"run_p :track{i}, track{i}, track{i}_name\n"

    return content

def run_command(user, cmd):
    try:
        command, track, position  = cmd.split(" ")
        if not command == "!play" and not command == "!stop":
            return

        # ignore this track item
        track = int(track)

        if len(tracks) <= track or track < 0:
            print(f"{user} Invalid Track {track}", flush=True)
            return

        position = int(position)

        t = tracks[track]
        if len(t) <= position or position < 0:
            print(f"{user} Invalid Position {position}", flush=True)
            return

        play = command == "!play"

        t[position] = 5 if play else 0
        return True

    except Exception as e:
        print(f"Nice try guy {user} {str(e)}")

    return False

COMMAND_TRIGGER = "!"

def is_command_msg(msg):
    return msg[0] == COMMAND_TRIGGER and msg[1] != COMMAND_TRIGGER

async def run_bot(twitch):
    music_server = await create_websocket(MUSIC_SERVER)
    ui_server = await create_websocket(UI_SERVER)

    # clear previous state
    await music_server.send(get_music())
    log("About to wait for ui server")
    await ui_server.send(get_state())
    log("Done waiting for ui servec")

    while True:
        # TODO: Make this async generator...
        log("Awaiting twitch message")
        user, msg = next(twitch)
        print("Got twitch message", msg, "from", user, flush=True)
        if user is not None and is_command_msg(msg):
            if run_command(user, msg):
                log("About to send music to music_server")
                await music_server.send(get_music())
                log("About to send state to state_server")
                await ui_server.send(get_state())
                log("Re-running twitch loop")

async def main():
    twitch = create_twitch_connection()
    await run_bot(twitch())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
