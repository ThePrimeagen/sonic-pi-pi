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

if "MUSIC_SERVER" not in os.environ:
    missing_env_var("MUSIC_SERVER")

if "UI_SERVER" not in os.environ:
    missing_env_var("UI_SERVER")

MUSIC_SERVER = os.environ["MUSIC_SERVER"]
UI_SERVER = os.environ["UI_SERVER"]

TOKEN = os.environ["TWITCH_OAUTH_TOKEN"]

# Note the bot name will not be what is specified here,
# unless the OAUTH token was generated for a Twitch Account with the same name.
BOT_NAME = os.environ["BOT_NAME"]

CHANNEL = os.environ["CHANNEL"]

ENCODING = "utf-8"
