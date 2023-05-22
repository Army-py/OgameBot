import discord
from discord.ext import commands
import datetime
import os 
from discord_slash import SlashContext, cog_ext



class CMD_load(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        __import__("is_ready").Is_Ready().command("load")



    options = [
    {
        "name":"cog",
        "description":"Cog",
        "type":3,
        "required":True,
        "choices":[]
    }]
    for filename in os.listdir("./cogs"): 
        if filename.endswith('.py'):
            (options[0])["choices"].append({
                "name":filename,
                "value":filename[:-3]
            })
    @cog_ext.cog_slash(name="load", description="Charger une extension", guild_ids=[799356517962874880], options=options)
    @commands.has_permissions(administrator=True)
    async def load(self, ctx, cog):
        try: 
            self.client.load_extension(f"cogs.{cog}")
            await ctx.send(f"{cog} chargé !")
            print(f"<{datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}> Load {cog}")
        except Exception as e: 
            await ctx.send(f"**Erreur pour `{cog}.py`**: {e}")
            print(e)




def setup(client):
    client.add_cog(CMD_load(client))