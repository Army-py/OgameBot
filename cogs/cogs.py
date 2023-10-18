import os

import discord
from discord.ext import commands


class Status:
    def __init__(self, client, cog):
        self.client = client
        self.cog = cog
        self.files = []
        self.files_status = []

    def sort_files(self):
        for filename in os.listdir("./cogs"):
            if self.cog in filename and filename not in self.files and filename.endswith('.py'):
                self.files.append(filename)


    async def get_status(self):
        for filename in self.files:
            try:
                await self.client.load_extension(f"cogs.{filename[:-3]}")
                cog = "`Unload 🔴`"
                await self.client.unload_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                e = str(e)
                if e.endswith("is already loaded."):
                    cog = "`Load 🟢`"
                else:
                    cog = "`Load Error 🟠`"
            self.files_status.append(f"➤ {filename[:-3]} {cog}")


    def set_embed(self):
        self.files_status.sort()
        self.embed = discord.Embed(
            title="Menu Cogs",
            color = discord.Color.from_rgb(255, 119, 0),
            description = "\n".join(self.files_status)
        )



class Cogs:
    def __init__(self, client):
        self.client = client
        self.files_status = []
        
        self.files_load = []
        self.files_load_error = []
        self.files_unload = []
        
        self.embed = discord.Embed(
            title="Menu Cogs",
            color = discord.Color.random(),
        )


    async def get_files(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith('.py'):
                try:
                    await self.client.load_extension(f"cogs.{filename[:-3]}")
                    self.files_unload.append(f"➥ {filename[:-3]} `Unload 🔴`")
                    await self.client.unload_extension(f"cogs.{filename[:-3]}")
                except Exception as e:
                    e = str(e)
                    if e.endswith("is already loaded."):
                        self.files_load.append(f"➥ {filename[:-3]} `Load 🟢`")
                    else:
                        self.files_load_error.append(f"➥ {filename[:-3]} `Load Error 🟠`")


    def set_embed(self, list, name, value):
        if len(list) > 10: self.embed.add_field(name=name, value=f"{value} : `{len(list)}`", inline=False)
        elif len(list) == 0: self.embed.add_field(name=name, value=f"{value} : `0`", inline=False)
        else: self.embed.add_field(name=name, value="\n".join(list), inline=False)



class CMD_cogs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        __import__("is_ready").Is_Ready().command("cogs")


    async def status(self, ctx, cog:str):
        s = Status(self.client, cog)
        s.sort_files()
        await s.get_status()
        s.set_embed()
        await ctx.send(embed=s.embed, delete_after=60)


    @commands.hybrid_command(aliases=["cog"], description="Affiche la liste des cogs")
    @commands.has_permissions(administrator=True)
    async def cogs(self, ctx: commands.Context, *, cog: str=None):
        # await ctx.message.delete()
        if cog is not None: return await self.status(ctx, cog)
        
        c = Cogs(self.client)
        await c.get_files()
        
        c.set_embed(c.files_load, "➤ Load", "➥ Load files")
        c.set_embed(c.files_load_error, "➤ Load Error", "➥ Load error files")
        c.set_embed(c.files_unload, "➤ Unload", "➥ Unload files")
        
        await ctx.send(embed=c.embed)
    

async def setup(client):
    await client.add_cog(CMD_cogs(client))
