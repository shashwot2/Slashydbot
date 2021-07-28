import discord
#import pandas
import random
from discord.ext import commands

client = commands.Bot(command_prefix='?')


@client.command(name="version")
async def version(context):
    VersionEmbed = discord.Embed(title="Current version", description="The bot is in beta", color=0x00f01)
    VersionEmbed.add_field(name="Owner", value="Slashd0t", inline=False)
    await context.channel.send(embed=VersionEmbed)


@client.event
async def on_ready():
    print('We have loggin as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Inventing skynet"))


@client.event
async def on_member_join(member):
    mbed = discord.Embed(
        colour=(discord.Colour.magenta()),
        title='Welcome Message',
        description=f'Welcome {member.mention}, enjoy your stay!'
    )
    await member.send(embed=mbed)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("hello"):
        await message.channel.send("Hello!")
    elif message.content.startswith("hola"):
        await message.channel.send("hola, amigo")
    elif message.content == "What is your version slashy d?":
        VersionEmbed = discord.Embed(title="Current version", description="The bot is in beta", color=0x00f01)
        VersionEmbed.add_field(name="Owner", value="Slashd0t", inline=False)
        await message.channel.send(embed=VersionEmbed)

    if message.content == "slashydbot is stupid":
        await message.author.send("Listen here you cheeky bastard")
    await client.process_commands(message)


@client.command(name="kick", pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
    await member.kick()
    await ctx.send("User {x} has been kicked".format(x=member.display_name))


@client.command(name="ban", pass_context=True)
@commands.has_permissions(kick_members=True)
async def ban(ctx, member: discord.Member, *, reason="Ask the admin"):
    await member.ban(reason=reason)
    await ctx.send("User {x} has been banned".format(x=member.display_name))
    await member.send("You are banned because{}".format(reason))


@client.command(name="dice", help='Rolls a 100 sided dice')
async def dice(ctx, amount: int = 1):
    diceEmbed = discord.Embed(title=f"Rolling for {ctx.message.author.display_name}", color=0xCC5500)

    for i in range(amount):
        roll = (random.randint(1, 100))
        diceEmbed.add_field(name=f"Roll number {i + 1}", value=roll, inline=False)
        if roll == 1:
            diceEmbed.set_footer(text="FUMBLE")

    await ctx.message.channel.send(embed=diceEmbed)


client.run('NzUxMDIxMzQ1ODE4NTQyMTIw.X1DBIg.LKDNb3Jyu1h5DODU5DD9SmKEljI')
