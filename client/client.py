import socket
import os


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


