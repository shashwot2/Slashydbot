from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
from Webserver import Webserver
import os

load_dotenv()
# Imports from __init__.py
from src import *

# Specifying intents to prevent the bot from monitoring everything
intents = Intents.default()
intents.typing = False
intents.presences = False
client = commands.Bot(command_prefix='?', intents=intents)

# Register the bot commands
client.add_command(pirate_ai)
client.add_command(version)
client.add_command(join)
client.add_command(play)
client.add_command(resume)
client.add_command(pause)
client.add_command(stop)
client.add_command(kick)
client.add_command(ban)
client.add_command(roman)
client.add_command(kanye)
client.add_command(dice)

# Register the bot events
client.event(on_ready)
client.event(on_member_join)
client.event(on_message)

Webserver()
client.run(os.getenv("DISCORD_APP_KEY"))