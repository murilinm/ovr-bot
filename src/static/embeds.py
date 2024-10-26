import discord

def rental_channel_embed(user_name: str, contact_info: str, people_in_house: int, renting_time: str, house_type: str, pets_in_house: bool):
    channel_embed = discord.Embed(title=f"Rental | {user_name}", description=f"You've opened a rental channel, please wait until one of our employees respond to this.\n\n**Contact Information:**\n```{contact_info}```\n\n**People in the house:\n```{people_in_house}```\n\n**Renting time:**\n```{renting_time}```\n\n**House type:**\n```{house_type}```\n\n**Will there be pets on the house?**\n```{pets_in_house}```") #,color=Hex code
    channel_embed.set_footer(text="Oceanpoint Vacation Rentals")
    return channel_embed