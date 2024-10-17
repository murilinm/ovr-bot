import discord
import responses

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

    @client.event
    async def on_message(message):
        try:
            user_message = str(message.content)
            if message.author == client.user or user_message[0] != "!": return
            print(user_message[0], user_message[1])
            #---------------!logrental--------------------
            if "!logrental" in user_message:
                try:
                    split = user_message.split(" ")
                except Exception as err:
                    return print(err)
                
                contents = {

                }

            #-----------hello--------------
            if user_message == "!hello":
                await message.channel.send(str("hello"))

            #-----------!cmds-------------
            if user_message == "!cmds":
                await message.channel.send("'!opa'; '!opa' [número até 500]; '!oopa' [número até 50], '!cmds'")

        except Exception as e:
            print(e)


    client.run(TOKEN)
