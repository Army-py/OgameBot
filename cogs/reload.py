import datetime
import os

import discord
from discord import app_commands
from discord.ext import commands


class CMD_reload(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        __import__("is_ready").Is_Ready().command("reload")


    
    # options = [
    # {
    #     "name":"cog",
    #     "description":"Cog",
    #     "type":3,
    #     "required":True,
    #     "choices":[]
    # }]
    # for filename in os.listdir("./cogs"): 
    #     if filename.endswith('.py'):
    #         (options[0])["choices"].append({
    #             "name":filename,
    #             "value":filename[:-3]
    #         })
    # @cog_ext.cog_slash(name="reload", description="Recharger une extension", guild_ids=[799356517962874880], options=options)
    # @commands.has_permissions(administrator=True)
    async def cog_autocomplete(self, interaction: discord.Interaction, current: str):
        cog_names = []
        for filename in os.listdir("./cogs"): 
            if filename.endswith('.py'):
                cog_names.append(filename[:-3])
        return [
            app_commands.Choice(name=cog_names[i], value=cog_names[i])
            for i in range(len(cog_names))
            if cog_names[i].lower().startswith(current.lower())
        ]
    
    # @cog_ext.cog_slash(name="load", description="Charger une extension", guild_ids=[799356517962874880], options=options)
    @app_commands.command(name="reload", description="Recharger une extension")
    @app_commands.autocomplete(cog=cog_autocomplete)
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx: discord.Interaction, cog: str):
        try:
            await self.client.reload_extension(f"cogs.{cog}")
            await ctx.response.send_message(f"{cog} rechargé !")
            print(f"<{datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}> Reload {cog}")
        except Exception as e:
            await ctx.response.send_message(f"**Erreur pour `{cog}.py`**: {e}")
            print(e)
            await self.client.unload_extension(f"cogs.{cog}")




async def setup(client):
    await client.add_cog(CMD_reload(client))