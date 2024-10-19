import discord
import logging
from discord.ext import commands
from discord import app_commands
from dpyConsole import Console

TOKEN = 'MTI5MTQyODg5NzY5ODc0MjMyMw.GZD3Y5.Z-X9A6puKGPLV3gej1y1YwOtHhCqGRpZFw1wDY'
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
bot = commands.Bot(command_prefix='!', intents=intents)
my_console = Console(client)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print("I'm Ready")

@my_console.command()
async def hey():
    print("fooe")
    bot.tree.copy_global_to(guild=discord.Object(id=int(1291429430895575080)))
    print("foo")
    await bot.tree.sync(guild=discord.Object(id=int(1291429430895575080)))
    print("tree synced")

@bot.tree.command(name="test", description="s")
async def test(interaction, arg1: str):
    print('foo')

my_console.start()
client.run(TOKEN, log_handler=handler)