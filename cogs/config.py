import json
import asyncio
from enum import Enum

import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext


class records(Enum):
    batiment_planetaire = "Bâtiment Planetaire"
    batiment_lunaire = "Bâtiment Lunaire"
    recherches = "Recherches"
    vaisseaux_militaires = "Vaisseaux Militaires"
    vaisseaux_civils = "Vaisseaux Civils"
    defense_planetaire = "Défense Planetaire"
    defense_lunaire = "Défense Lunaire"



class Command:
    def __init__(self, client, config, record, value):
        self.client = client
        self.config = config
        self.record = record
        self.value = value

        self.embed = discord.Embed(
            title="Configuration actuelle",
            colour=discord.Colour.random()
            )


    def set_embed(self):
        with open("./config/config.json", "r") as file:
            config = json.load(file)
            for i in config:
                if i == "refresh_time":
                    self.embed.add_field(name="Temps d'actualisation", value=f"`{config.get(i)}` secondes", inline=False)
                else:
                    self.embed.add_field(name=records[i].value, value=f"Plage : `{(config.get(i))['range']}`\nCouleur de l'embed : `RGB{str((config.get(i))['color']).replace('[', '(').replace(']', ')')}`\nCouleur du texte : `{(config.get(i))['prefix']}`", inline=True)


    async def update_value(self):
        with open("./config/config.json", "r") as file:
            config = json.load(file)
            if self.config == "color":
                colors = (self.value).replace(" ", "").split(",")
                for i in range(len(colors)): colors[i] = int(colors[i])
                (config[self.record])[self.config] = colors
            elif self.config == "refresh_time":
                (config[self.config]) = float(self.value)
            else:
                (config[self.record])[self.config] = str(self.value)
        
        with open("./config/config.json", "w") as file:
            json.dump(config, file, indent=4)
        if self.config == "refresh_time": 
            await asyncio.sleep(1)
            self.client.reload_extension(f"cogs.refresh")



class CMD_config(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        __import__("is_ready").Is_Ready().command("config")


    options = [
        {
            "name":"config",
            "description":"Choix des configurations",
            "required":True,
            "type":3,
            "choices":[
                {
                    "name":"Afficher la configuration actuelle",
                    "value":"all"
                },
                {
                    "name": "Temps d'actualisation",
                    "value": "refresh_time"
                },
                {
                    "name": "Plage de cellules",
                    "value": "range"
                },
                {
                    "name": "Couleur de l'embed",
                    "value": "color"
                },
                {
                    "name": "Couleur du texte",
                    "value": "prefix"
                }]
        },
        {
            "name":"records",
            "description":"Choix des records",
            "required": False,
            "type":3,
            "choices":[
                {
                    "name": "Batiment Planetaire",
                    "value": "batiment_planetaire"
                },
                {
                    "name": "Batiment Lunaire",
                    "value": "batiment_lunaire"
                },
                {
                    "name": "Recherches",
                    "value": "recherches"
                },
                {
                    "name": "Vaisseaux Militaires",
                    "value": "vaisseaux_militaires"
                },
                {
                    "name": "Vaisseaux Civils",
                    "value": "vaisseaux_civils"
                },
                {
                    "name": "Défense Planetaire",
                    "value": "defense_planetaire"
                },
                {
                    "name": "Défense Lunaire",
                    "value": "defense_lunaire"
                }]
        },
        {
            "name":"value",
            "description":"Nouvelle valeur de la configuration",
            "required":False,
            "type":3
        }
    ]
    @cog_ext.cog_slash(name="config", description="Configuration du bot", guild_ids=[799356517962874880], options=options)
    @commands.has_permissions(administrator=True)
    async def config(self, ctx:SlashContext, config, record=None, value=None):
        cmd = Command(self.client, config, record, value)
        if config == "all":
            cmd.set_embed()
            await ctx.send(embed=cmd.embed)
        else:
            await cmd.update_value()
            await ctx.send(f"La valeur a été modifiée", delete_after=5)



def setup(client):
    client.add_cog(CMD_config(client))
