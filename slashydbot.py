import discord
import os
#import pandas
import random
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL

client = commands.Bot(command_prefix='?')

players = {}
# This function returns the version of the bot to the user, also displays the owner the bot


@client.command(name="version")
async def version(context):
    VersionEmbed = discord.Embed(
        title="Current version", description="The bot is in beta", color=0x00f01)
    VersionEmbed.add_field(name="Owner", value="Slashd0t", inline=False)
    await context.channel.send(embed=VersionEmbed)

# this function has the bot join the voice channel the bot is in


@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

# Plays sound from youtube URL


@client.command()
async def play(ctx, url):
    DL_OPTIONS = {'format': 'bestaudio/best',
                  'noplaylist': True,
                  'extractaudio': True,
                  'audioformat': 'mp3'
                  }
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_deplay_max 5',
        'options': '-vn'
    }
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(DL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('bot is playing')

    else:
        await ctx.send("Bot is already playing")
        return

# Displays currently idle and the game playing


@client.event
async def on_ready():
    print('We have loggin as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Inventing skynet"))

# Displays welcome message on joining the discord server the bot is currently located in


@client.event
async def on_member_join(member):
    mbed = discord.Embed(
        colour=(discord.Colour.magenta()),
        title='Welcome Message',
        description=f'Welcome {member.mention}, enjoy your stay!'
    )
    await member.send(embed=mbed)

# This function returns appopriate output to the input by the users, for example it says hello if the users says hello


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
            title="Current version", description="The bot is in beta", color=0x00f01)
        VersionEmbed.add_field(name="Owner", value="Slashd0t", inline=False)
        await message.channel.send(embed=VersionEmbed)

    if message.content == "slashydbot is stupid":
        await message.author.send("Please don't insult me :), im sure you're a great person")
    await client.process_commands(message)

# kicks the member provided the user using it has permission to kick the person


@client.command(name="kick", pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
    await member.kick()
    await ctx.send("User {x} has been kicked".format(x=member.display_name))

# bans the member provided the user using it has the permission to ban the person


@client.command(name="ban", pass_context=True)
@commands.has_permissions(kick_members=True)
async def ban(ctx, member: discord.Member, *, reason="Ask the admin"):
    await member.ban(reason=reason)
    await ctx.send("User {x} has been banned".format(x=member.display_name))
    await member.send("You are banned because{}".format(reason))
#TODO: BLACKJACK
# @client.command(name="blackjack", help= "plays blackjack")
# async def blackjack(ctx):


# This function returns the roman numeral's value
@client.command(name="roman", help="roman converter")
# dervied from https://github.com/shashwot2/vigilant-succotash/blob/main/Romannumerals.py
async def roman(ctx, num):
    positives = 0
    negatives = 0
    # Dictionary for Allocating each roman numeral
    dict = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    # processing if there is only one element
    if len(num) == 1:
        return dict[num[0]]
    # loops till the end of the string
    # Note that this converter does NOT detect if the certain numeral is not valid,
    for i in range(len(num)-1):
        # Comparing one element to the other and if it detects a negative it adds it to negatives
        if dict[num[i]] < dict[num[i+1]]:
            negatives = negatives + dict[num[i]]
        elif dict[num[i]] >= dict[num[i+1]]:
            positives = positives + dict[num[i]]
    positives = positives + dict[num[len(num)-1]]

    await ctx.message.channel.send(positives - negatives)
# TODO: make this below function workable, currently doesn't support as int and string
# @client.command(name = "secondstohours",help = "Converts seconds to hours, minutes and remanining to seconds based on the format 00:00:00")
# async def secondstohours(ctx,num):
#    temp_sec = num
#    minutes = int((num / 60) % 60)
 #   hours = int(num / 3600)
 #   num = int(temp_sec % 3600)
 #   if num >= 60:
#        seconds = num % 60
#    g = str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
#    await ctx.message.channel.send(g)


@client.command(name="dice", help='Rolls a dice, Please input a number,Then input the side of the dice ')
async def dice(ctx, amount: int = 1, sides: int = 6):
    diceEmbed = discord.Embed(
        title=f"Rolling for {ctx.message.author.display_name}", color=0xCC5500)

    for i in range(amount):
        roll = (random.randint(1, sides))
        diceEmbed.add_field(
            name=f"Roll number {i + 1}", value=roll, inline=False)
        if roll == 1:
            diceEmbed.set_footer(text="FUMBLE")

    await ctx.message.channel.send(embed=diceEmbed)


client.run('')