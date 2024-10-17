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
            nopa = ""
            noopa = ""

            #-----------------!opa--------------------------------------
            if "!opa" in user_message:
                try:
                    nopa = int(user_message.split(" ")[1])
                except Exception as e:
                    print()

                if nopa and str(type(nopa)) == "<class 'int'>":
                    if nopa >= 500:
                        return

                    if "!opa" in user_message:
                        await message.channel.send(str("opa " * nopa))

            #---------------!oopa--------------------
            if "!oopa" in user_message:
                try:
                    noopa = int(user_message.split(" ")[1])
                except Exception as err:
                    print()
                if noopa and str(type(noopa)) == "<class 'int'>":
                    if noopa >= 50:
                        return

                    if "!oopa" in user_message:
                        await message.channel.send(str("o" * noopa + "opa"))

            #-----------!opa--------------
            if user_message == "!opa":
                await message.channel.send(str("opa"))

            #-----------!cmds-------------
            if user_message == "!cmds":
                await message.channel.send("'!opa'; '!opa' [número até 500]; '!oopa' [número até 50], '!cmds'")

        except Exception as e:
            print(e)


    client.run(TOKEN)
