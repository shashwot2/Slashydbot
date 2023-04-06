import random
import requests
import discord
from youtube_dl import YoutubeDL
from discord.utils import get
from openai_commands import pirate_ai

# Pass client to every function at once


def register_bot_commands(client):
    client.command(name="version", help="Prints version of bot")(version)
    # client.command(
    #     name="join",
    #     help="Joins the bot to the voice channel ")(join)
    # client.command(name="play", help="Plays the specified song")(play)
    client.command(
        name="resume",
        help="Resumes the song that has been paused")(resume)
    client.command(
        name="pause",
        help="Pauses the song that is currently playing")(pause)
    client.command(name="stop", help="stops the song that's playing")(stop)
    client.command(
        name="roman",
        help="Converts a Roman numeral to a Hindu-Arabic numeral")(roman)
    client.command(
        name="kanye",
        help="Queries a free api to generate a random kanye quote")(kanye)
    client.command(
        name="dice",
        help="Rolls a dice. First input is number of dice(default 1) and 2nd is custom dice size(default 6)")(dice)
    client.command(
        name="pirate-ai",
        help="This command will pretend it's a pirate(uses gpt3.5)")(pirate_ai)


# This function returns the version of the bot to the user, also displays
# the owner the bot
async def version(context):
    VersionEmbed = discord.Embed(
        title="Current version",
        description="The bot is in beta",
        color=0x00f01)
    VersionEmbed.add_field(name="Owner", value="Slashd0t", inline=False)
    await context.channel.send(embed=VersionEmbed)


async def join(client, ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

# This discord play feature is forked from :
# https://github.com/eric-yeung/Discord-Bot


async def play(client, ctx, url):
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_deplay_max 5',
        'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(DL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('bot is playing')

    else:
        await ctx.send("Bot is already playing")
        return


async def resume(ctx):
    voice = ctx.message.guild.voice_client
    if voice.is_paused():
        voice.resume()
        await ctx.send("Resuming")
    else:
        await ctx.send("The bot was not playing anything before this. Use play command")


async def pause(client, ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Bot has been paused')


async def stop(ctx):
    voice = ctx.message.guild.voice_client
    if voice.is_playing():
        voice.stop()
        await ctx.send("The bot is stopping")
    else:
        await ctx.send("The bot is not playing anything at the moment.")

# Note that this converter does NOT detect if the certain numeral is not valid,


async def roman(ctx, num):
    positives = 0
    negatives = 0
    dict = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    if len(num) == 1:
        return dict[num[0]]
    # loops till the end of the string
    for i in range(len(num) - 1):
        # Comparing one element to the other and if it detects a negative it
        # adds it to negatives
        if dict[num[i]] < dict[num[i + 1]]:
            negatives = negatives + dict[num[i]]
        elif dict[num[i]] >= dict[num[i + 1]]:
            positives = positives + dict[num[i]]
    positives = positives + dict[num[len(num) - 1]]

    await ctx.message.channel.send(positives - negatives)


async def kanye(ctx):
    url = "https://api.kanye.rest"
    response = requests.get(url)
    data = response.json()
    await ctx.message.channel.send(data["quote"])


async def dice(ctx, amount: int = 1, sides: int = 6):
    diceEmbed = discord.Embed(
        title=f"Rolling for {ctx.message.author.display_name}", color=0xCC5500)

    for i in range(amount):
        roll = (random.randint(1, sides))
        diceEmbed.add_field(
            name=f"Roll number {i + 1}", value=roll, inline=False)
    await ctx.message.channel.send("Rolling " + str(sides) + " sided dice")

    await ctx.message.channel.send(embed=diceEmbed)
