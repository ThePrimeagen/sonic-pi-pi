import socket
import os

print("return server")

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


TOKEN = os.environ["TWITCH_OAUTH_TOKEN"]

# Note the bot name will not be what is specified here,
# unless the OAUTH token was generated for a Twitch Account with the same name.
BOT_NAME = os.environ["BOT_NAME"]

CHANNEL = os.environ["CHANNEL"]

ENCODING = "utf-8"

# Define your own trigger for commands:
COMMAND_TRIGGER = "!"

print("next to comment outs")
def _handshake(server):
    print(f"Connecting to #{CHANNEL} as {BOT_NAME}")
    print(server.send(bytes("PASS " + TOKEN + "\r\n", ENCODING)))
    print(server.send(bytes("NICK " + BOT_NAME + "\r\n", ENCODING)))
    print(server.send(bytes("JOIN " + f"#{CHANNEL}" + "\r\n", ENCODING)))


def _connect_to_twitch():
    print("Connecting")
    connection_data = ("irc.chat.twitch.tv", 6667)
    print("creating server socket")
    server = socket.socket()
    print("connecting")
    server.connect(connection_data)
    print("_handshake")
    _handshake(server)
    print("return server")
    return server


def pong(server):
    server.sendall(bytes("PONG" + "\r\n", ENCODING))


def send_message(server, msg):
    server.send(bytes("PRIVMSG " + f"#{CHANNEL}" + " :" + msg + "\n", ENCODING))

def _is_command_msg(msg):
    return msg[0] == COMMAND_TRIGGER and msg[1] != COMMAND_TRIGGER


def process_msg(irc_response):
    # TODO: improve the specificity of detecting Pings
    if "PING" in irc_response:
        pong(server)

    split_response = irc_response.split()

    if len(split_response) < 4:
        return

    user, msg = _parse_user_and_msg(irc_response)

    if _is_command_msg(msg):
        print(f"We want to run command {msg}")
    else:
        print(f"{user}: {msg}")


# TODO: refactor this sillyness
def _parse_user_and_msg(irc_response):
    user_info, _, _, *raw_msg = irc_response.split()
    raw_first_word, *raw_rest_of_the_message = raw_msg
    first_word = raw_first_word[1:]
    rest_of_the_message = " ".join(raw_rest_of_the_message)
    user = user_info.split("!")[0][1:]
    msg = f"{first_word} {rest_of_the_message}"
    return user, msg


def run_bot(server):
    chat_buffer = ""

    while True:
        print("HELLO, I am true!")
        chat_buffer = chat_buffer + server.recv(2048).decode("utf-8")
        messages = chat_buffer.split("\r\n")
        print("Messages, ", messages)
        chat_buffer = messages.pop()

        for message in messages:
            process_msg(message)


if __name__ == "__main__":
    server = _connect_to_twitch()
    send_message(server, "Hello")
    # run_bot(server)

print("bottom of the file")
