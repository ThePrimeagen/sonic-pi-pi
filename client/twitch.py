import socket
import asyncio
import os
from utils import TOKEN, BOT_NAME, CHANNEL, ENCODING

def create_twitch_connection(): 

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

    def process_msg(irc_response, server):
        # TODO: improve the specificity of detecting Pings
        if "PING" in irc_response:
            pong(server)

        split_response = irc_response.split()

        print(f"Messages from the twitch {split_response}")
        if len(split_response) < 4:
            return None, None

        user, msg = _parse_user_and_msg(irc_response)
        return user.strip(), msg.strip()


# TODO: refactor this sillyness
    def _parse_user_and_msg(irc_response):
        user_info, _, _, *raw_msg = irc_response.split()
        raw_first_word, *raw_rest_of_the_message = raw_msg
        first_word = raw_first_word[1:]
        rest_of_the_message = " ".join(raw_rest_of_the_message)
        user = user_info.split("!")[0][1:]
        msg = f"{first_word} {rest_of_the_message}"
        return user, msg


    def read_from_twitch():
        twitch = _connect_to_twitch()
        messages = []
        chat_buffer = ""

        while True:
            if len(messages) > 0:
                yield process_msg(messages.pop(), twitch)

            chat_buffer = chat_buffer + twitch.recv(2048).decode("utf-8")
            messages = chat_buffer.split("\r\n")

            if not chat_buffer.endswith("\r\n"):
                chat_buffer = messages.pop()
            else:
                chat_buffer = ""

            if len(messages) > 0:
                yield process_msg(messages.pop(), twitch)

    return read_from_twitch

COMMAND_TRIGGER = "!"

def is_command_msg(msg: str) -> str:
    return msg[0] == COMMAND_TRIGGER and msg[1] != COMMAND_TRIGGER

