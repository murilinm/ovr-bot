import discord

def rental_channel(user_name: str, contact_info: str, people_in_house: int, renting_time: str, house_type: str, pets_in_house: bool):
    channel_embed = discord.Embed(title=f"Rental | {user_name}", description=f"You've opened a rental channel, please wait until one of our employees respond to this. If you opened this accidentally, please let us know.\n\n**Contact Information:**\n```{contact_info}```\n\n**People in the house:**\n```{people_in_house}```\n\n**Renting time:**\n```{renting_time}```\n\n**House type:**\n```{house_type}```\n\n**Will there be pets on the house?**\n```{pets_in_house}```") #,color=Hex code
    channel_embed.set_footer(text="Oceanpoint Vacation Rentals")
    return channel_embed

def general_ticket_channel(user_name):
    embed=discord.Embed(title=f"General ticket | {user_name}", description="You've opened a general ticket, please let us know what you need help with. If you opened this accidentally, please let us know.")
    embed.set_footer(text="Oceanpoint Vacation Rentals")
    return embed

def management_ticket_channel(user_name):
    embed=discord.Embed(title=f"Management ticket | {user_name}", description="You've opened a management ticket, please use the format below and wait for one of our staff to respond. If you opened this accidentally, please let us know.\n\n```Discord User:\nReason:\nEvidence:```")
    embed.set_footer(text="Oceanpoint Vacation Rentals")
    return embed