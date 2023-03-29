import discord
from discord.ext import commands


def register_bot_admin_commands(client):
    client.command(name="kick", pass_context=True)(kick)
    client.command(name="ban", pass_context=True)(ban)


@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
    await member.kick()
    await ctx.send("User {x} has been kicked".format(x=member.display_name))


@commands.has_permissions(kick_members=True)
async def ban(ctx, member: discord.Member, *, reason="Ask the admin"):
    await member.ban(reason=reason)
    await ctx.send("User {x} has been banned".format(x=member.display_name))
    await member.send("You are banned because{}".format(reason))
