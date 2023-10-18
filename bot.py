import datetime
import json
import os
from pathlib import Path

import discord
from discord.ext import commands

cwd = Path(__file__).parents[0]
cwd = str(cwd)

class OgameBot(commands.Bot):
    def __init__(self):
        activity=discord.Activity(type=discord.ActivityType.watching)
        
        super().__init__(
            command_prefix="/",
            owner_id=338046587337048064,
            intents=discord.Intents().all(),
            activity=activity,
            case_insensitive=True
        )
    
    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    # client.load(f"cogs.{filename[:-3]}")
                except Exception as e:
                    print(e)
        await self.tree.sync()

client = OgameBot()
secret_file = json.load(open(cwd+'/bot_config/secret.json'))
client.config_token = secret_file['token']
client.remove_command('help')


async def is_owner(ctx):
    return ctx.author.id == 338046587337048064

@client.event
async def on_ready():
    print(f"<{datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}> Bot is ready")


client.run(client.config_token)
