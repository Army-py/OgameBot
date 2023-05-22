import datetime
import json
import os
from pathlib import Path

import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext


cwd = Path(__file__).parents[0]
cwd = str(cwd)

client = commands.Bot(command_prefix="/", intents=discord.Intents.all())
slash = SlashCommand(client, override_type = True, sync_commands=True, sync_on_cog_reload=True)
secret_file = json.load(open(cwd+'/bot_config/secret.json'))
client.config_token = secret_file['token']
client.remove_command('help')

for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        try:
            client.load_extension(f"cogs.{filename[:-3]}")
        except Exception as e:
            print(e)

async def is_owner(ctx):
    return ctx.author.id == 338046587337048064

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="mettre les records à jour"))
    print(f"<{datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}> Bot is ready")


client.run(client.config_token)
