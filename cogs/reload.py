import discord
from discord.ext import commands
import datetime

class CMD_reload(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog):
        await ctx.message.delete()
        try:
            self.client.reload_extension(f"cogs.{cog}")
            print(f"<{datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}> Reload {cog}")
        except Exception as e:
            self.client.unload_extension(f"cogs.{cog}")




def setup(client):
    client.add_cog(CMD_reload(client))