import discord.ext.test as dpytest
import asyncio
import pytest
import pytest_asyncio
import discord
from discord import Intents
from discord.ext import commands

from src.bot_commands import roman
@pytest_asyncio.fixture
async def bot():
    intents = Intents.default()
    intents.typing = False
    intents.presences = False
    intents.message_content = True
    bot = commands.Bot(command_prefix="?", intents=intents)
    await bot._async_setup_hook()
    dpytest.configure(bot)
    return bot


@pytest.mark.asyncio
async def test_roman(bot):
    dpytest.configure(bot)
    test_cases = [
        ('I', 1),
        ('II', 2),
        ('IV', 4),
        ('V', 5),
        ('VI', 6),
        ('IX', 9),
        ('X', 10),
        ('XI', 11),
        ('IL', 49),
        ('L', 50),
        ('LX', 60),
        ('IC', 99),
        ('MCMXCIV ', 1994),
    ]

    for romanNumeral, expectedValue in test_cases:
        await dpytest.message(f'?roman {romanNumeral}')
        assert dpytest.verify_message(expectedValue)
        dpytest.empty_queue()
        