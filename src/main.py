import discord
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
import os
from discord.utils import get
import youtube_dl

# local imports
from bot_commands import register_bot_commands
from bot_admin_commands import register_bot_admin_commands
from Webserver import Webserver

load_dotenv()

# Specifying intents to prevent the bot from monitoring everything
intents = Intents.default()
intents.typing = False
intents.presences = False
# intents.message_content = True
intents.voice_states= True
client = commands.Bot(command_prefix='?', intents=intents)

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_deplay_max 5',
    'options': '-vn'}

YDL_OPTIONS = {'format': 'bestaudio/best',
                'noplaylist': True,
                'extractaudio': True,
                'audioformat': 'mp3',
                'outtmpl': 'downloads/%(title)s-%(ext)s',
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'logtostderr': False,
                'quiet': False,
                'no_warnings': False,
                'default_search': 'auto',
                'source_address': '0.0.0.0',
                'verbose': True,
                }

ydl = youtube_dl.YoutubeDL(YDL_OPTIONS)

@client.command(name="play")
async def play(ctx, *, url):
        with ydl:
            info = ydl.extract_info(url, download=False)
            URL2 = info['formats'][0]['url']
        FFMPEG_OPTIONS['options'] = '-vn'
        voice_client = ctx.voice_client
        voice_client.stop()
        voice_client.play(discord.FFmpegPCMAudio(URL2, **FFMPEG_OPTIONS))

@client.command(name= "join")
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

register_bot_commands(client)
register_bot_admin_commands(client)

# Monitoring events in main to reduce complexity of implementing in
# another file


@client.event
async def on_ready():
    print('We have loggin as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Inventing skynet"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("hello"):
        await message.channel.send("Hello!")
    elif message.content.startswith("hola"):
        await message.channel.send("hola, amigo")
    elif message.content == "What is your version slashy d?":
        VersionEmbed = discord.Embed(
            title="Current version",
            description="The bot is in beta",
            color=0x00f01)
        VersionEmbed.add_field(name="Owner", value="Slashd0t", inline=False)
        await message.channel.send(embed=VersionEmbed)

    if message.content == "slashydbot is stupid":
        await message.author.send("Please don't insult me :), im sure you're a great person")
    await client.process_commands(message)


@client.event
async def on_member_join(member):
    mbed = discord.Embed(
        colour=(discord.Colour.magenta()),
        title='Welcome Message',
        description=f'Welcome {member.mention}, enjoy your stay!'
    )
    await member.send(embed=mbed)

Webserver()
client.run(os.getenv("DISCORD_APP_KEY"))
