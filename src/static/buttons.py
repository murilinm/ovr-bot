import discord
from discord.ui import Button, View
from global_variables import global_variables

def rental_channel_button(guild_id: int, channel_id: int):
    channel_button = Button(label='Go to rental channel', url=f'https://discord.com/channels/{guild_id}/{channel_id}')
    view=View()
    view.add_item(channel_button)
    return view

def rental_close_button():
    close_button=Button(style=discord.ButtonStyle.danger, label='Close', custom_id='rental_close_button', emoji='🔒')
    
    async def callback(interaction):
        await interaction.response.send_message("Closing channel, please wait...")
        await interaction.channel.delete(reason=f"User {interaction.user.name} (ID: {interaction.user.id}) clicked the 'Close' button")
        global_variables.delete_key("global_variables/openedRentals.json", interaction.channel_id)

    close_button.callback=callback

    view=View()
    view.add_item(close_button)
    return view