import socket
import os
import asyncio
import websockets

async def create_websocket(server):
    uri = f"ws://{server}:42069"
    return await websockets.connect(uri) 

def log(string): 
    print(string, flush=True)

def missing_env_var(var_name):
    raise ValueError(
        (
            f"Please populate the {var_name} environment variable to run the bot. "
            "See README for more details."
        )
    )


# Get the value for this here: https://twitchapps.com/tmi/
if "TWITCH_OAUTH_TOKEN" not in os.environ:
    missing_env_var("TWITCH_OAUTH_TOKEN")

if "BOT_NAME" not in os.environ:
    missing_env_var("BOT_NAME")

if "CHANNEL" not in os.environ:
    missing_env_var("CHANNEL")

if "SERVER" not in os.environ:
    missing_env_var("SERVER")

SERVER = os.environ["SERVER"]

TOKEN = os.environ["TWITCH_OAUTH_TOKEN"]

# Note the bot name will not be what is specified here,
# unless the OAUTH token was generated for a Twitch Account with the same name.
BOT_NAME = os.environ["BOT_NAME"]

CHANNEL = os.environ["CHANNEL"]

ENCODING = "utf-8"

# Define your own trigger for commands:
COMMAND_TRIGGER = "!"

def _handshake(server):
    print(f"Connecting to #{CHANNEL} as {BOT_NAME}")
    print(server.send(bytes("PASS " + TOKEN + "\r\n", ENCODING)))
    print(server.send(bytes("NICK " + BOT_NAME + "\r\n", ENCODING)))
    print(server.send(bytes("JOIN " + f"#{CHANNEL}" + "\r\n", ENCODING)))


def _connect_to_twitch():
    connection_data = ("irc.chat.twitch.tv", 6667)
    server = socket.socket()
    server.connect(connection_data)
    _handshake(server)
    return server


def pong(server):
    server.sendall(bytes("PONG" + "\r\n", ENCODING))


def send_message(server, msg):
    server.send(bytes("PRIVMSG " + f"#{CHANNEL}" + " :" + msg + "\r\n", ENCODING))

def is_command_msg(msg):
    return msg[0] == COMMAND_TRIGGER and msg[1] != COMMAND_TRIGGER

def run_command(websocket, user, cmd):
    return

def process_msg(irc_response):
    # TODO: improve the specificity of detecting Pings
    if "PING" in irc_response:
        pong(server)

    split_response = irc_response.split()

    if len(split_response) < 4:
        return None, None

    user, msg = _parse_user_and_msg(irc_response)
    return user, msg


# TODO: refactor this sillyness
def _parse_user_and_msg(irc_response):
    user_info, _, _, *raw_msg = irc_response.split()
    raw_first_word, *raw_rest_of_the_message = raw_msg
    first_word = raw_first_word[1:]
    rest_of_the_message = " ".join(raw_rest_of_the_message)
    user = user_info.split("!")[0][1:]
    msg = f"{first_word} {rest_of_the_message}"
    return user, msg


async def run_bot(server):
    chat_buffer = ""
    websocket = await create_websocket(SERVER)

    while True:
        chat_buffer = chat_buffer + server.recv(2048).decode("utf-8")
        messages = chat_buffer.split("\r\n")
        chat_buffer = messages.pop()

        for message in messages:
            user, msg = process_msg(message)
            if user is not None and is_command_msg(msg):
                run_command(user, msg)

async def main():
    server = _connect_to_twitch()
    await run_bot(server)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


