import discord, json, asyncio
from discord.ui import Button, View
from global_variables import global_variables
from static import embeds
from imports import tst

# VARIABLES
# - TEST SERVER
test_guild_id=1291429430895575080
test_tickets_cat_id=1292466525998940244
test_roles = {
    "employee": 1291826425430806669,
    "member": 1302266854525632532,
    "unverified": 1302266912784515082,
    "hr": 1302267093076676608,
    "master_contractor": 1302267042015084648
}

# - MAIN SERVER

global gdb,mdb
gdb=mdb=False

# FUNCTIONS


