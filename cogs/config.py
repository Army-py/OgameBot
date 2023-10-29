import asyncio
import json

import discord
from discord import app_commands
from discord.ext import commands


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
        with open("./config/config.json", "r", encoding="utf8") as file:
            config = json.load(file)
            if "refresh_time" in config.keys():
                self.embed.add_field(name="Temps d'actualisation", value=f"`{config['refresh_time']}` secondes", inline=False)
            
            for i in config["structure"].keys():
                if i == "*": continue
                else: self.embed.add_field(name=config['structure'][i]['name'], value=f"Plage : `{config['structure'][i]['range']}`\nCouleur de l'embed : `RGB{str(config['structure'][i]['color']).replace('[', '(').replace(']', ')')}`\nCouleur du texte : `{config['structure'][i]['prefix']}`", inline=True)


    async def update_value(self):
        with open("./config/config.json", "r", encoding="utf8") as file:
            config = json.load(file)
            if self.config == "color":
                colors = (self.value).replace(" ", "").split(",")
                for i in range(len(colors)): colors[i] = int(colors[i])
                config["structure"][self.record][self.config] = colors
            elif self.config == "refresh_time":
                config[self.config] = float(self.value)
            else:
                config["structure"][self.record][self.config] = str(self.value)
        
        with open("./config/config.json", "w", encoding="utf8") as file:
            json.dump(config, file, indent=4)
        await asyncio.sleep(1)
        if self.config == "refresh_time": 
            await self.client.reload_extension(f"cogs.refresh")
        await self.client.reload_extension(f"cogs.config")



class CMD_config(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = json.load(open("./config/config.json", encoding="utf8"))


    @commands.Cog.listener()
    async def on_ready(self):
        __import__("is_ready").Is_Ready().command("config")


    async def config_autocomplete(self, interaction: discord.Interaction, current: str):
        # config_names = ["Afficher la configuration actuelle", "Temps d'actualisation", "Plage de cellules", "Couleur de l'embed", "Couleur du texte", "Nom des bâtiments"]
        # config_values = ["*", "refresh_time", "range", "color", "prefix", "name"]
        config_keys = [k for k in self.config["config"].keys()]
        config_values = [self.config["config"][k] for k in config_keys]
        return [
            app_commands.Choice(name=config_values[i], value=config_keys[i])
            for i in range(len(config_values))
            if config_values[i].lower().startswith(current.lower())
        ]
    
    async def record_autocomplete(self, interaction: discord.Interaction, current: str):
        record_names = [self.config["structure"][k]["name"] for k in self.config["structure"].keys()]
        record_keys = [k for k in self.config["structure"].keys()]
        record_names.pop(record_keys.index("*"))
        record_keys.remove("*")
        return [
            app_commands.Choice(name=record_names[i], value=record_keys[i])
            for i in range(len(record_names))
            if record_names[i].lower().startswith(current.lower())
        ]
    

    @app_commands.command(name="config", description="Configuration du bot")
    @app_commands.autocomplete(config=config_autocomplete, record=record_autocomplete)
    @commands.has_permissions(administrator=True)
    async def config_command(self, interaction: discord.Interaction, config: str, record: str = None, value: str=None):
        cmd = Command(self.client, config, record, value)
        if config == "*":
            cmd.set_embed()
            await interaction.response.send_message(embed=cmd.embed)
        else:
            await cmd.update_value()
            await interaction.response.send_message("La valeur a été modifiée")



async def setup(client):
    await client.add_cog(CMD_config(client))
