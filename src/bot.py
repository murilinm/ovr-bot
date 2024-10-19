import discord
import responses
from discord.ext import commands

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response)

    except Exception as e:
        print(e)

def run_bot():
    TOKEN = 'MTI5MTQyODg5NzY5ODc0MjMyMw.GZD3Y5.Z-X9A6puKGPLV3gej1y1YwOtHhCqGRpZFw1wDY'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.command()
    async def test(ctx, arg):
        await ctx.send(arg)




@bot.command(name='hey')
async def _hey(ctx, arg):
    print("command")
    await ctx.send('hii')


    client.run(TOKEN)