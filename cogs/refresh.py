import json
import sys
from enum import Enum

import discord
from discord import app_commands
from discord.ext import commands, tasks
from google.oauth2 import service_account
from googleapiclient.discovery import build


class prefixes(Enum):
    md = "#"
    diff = "-"


class Listener:
    def __init__(self, client):
        self.client = client
        self.SAMPLE_SPREADSHEET_ID_input = '1gW7Q4xEHGw_aSez9UuQCjG8CHoa3R0EGO2IWivp1720'


    async def connect(self):
        try:
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

            credentials = None
            credentials = service_account.Credentials.from_service_account_file('./bot_config/credentials.json', scopes=SCOPES)

            service = build('sheets', 'v4', credentials=credentials)

            # Call the Sheets API
            self.sheet = service.spreadsheets()
        except Exception as e:
            print(f"--- {e}")


    def get_values(self, range):
        result_input = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID_input,
                            range=range).execute()
        values_input = result_input.get('values', [])
        return values_input


    def format_values(self, range):
        data = []
        for i in self.get_values((self.config[range])["range"]):
            data.append(' - '.join([f"{lst}" for lst in i]))
        return data


    def open_config(self):
        file = open("./config/config.json")
        self.config = json.load(file)


    def get_color(self, range):
        self.color = (self.config[range])["color"]


    def get_language(self, range):
        self.language = (self.config[range])["prefix"]


    def set_embed(self, range):
        self.open_config()
        self.get_color(range)
        self.get_language(range)

        if self.language in prefixes.__members__: prefix = prefixes[self.language].value
        else: prefix = ""

        self.embed = discord.Embed(
            description = f"```{self.language}\n" + '\n'.join([f"{prefix} {lst}" for lst in self.format_values(range)]) + "\n```",
            colour = discord.Colour.from_rgb(self.color[0], self.color[1], self.color[2])
        )
        # self.embed.set_image(url=f"attachment://{range}.png")
        return self.embed


    def update_message_id(self, msg, range):
        with open("./files/json/messages.json", "r") as file:
            messages_id = json.load(file)
            (messages_id[range])["message_id"] = msg.id
            (messages_id[range])["channel_id"] = msg.channel.id
        
        with open("./files/json/messages.json", "w") as file:
            json.dump(messages_id, file, indent=4)


    async def send(self, ctx: discord.Interaction, type):
        image = discord.File(f"./files/images/{type}.png", filename=f"{type}.png")
        msg = await ctx.channel.send(file=image, embed=self.set_embed(type))
        self.update_message_id(msg, type)


    # async def follow(self, ctx: discord.Interaction, type):
    #     image = discord.File(f"./files/images/{type}.png", filename=f"{type}.png")
    #     msg = await ctx.followup.send(file=image, embed=self.set_embed(type))
    #     self.update_message_id(msg, type)


    async def refresh(self):
        with open("./files/json/messages.json", "r") as file:
            messages_id = json.load(file)
            for i in messages_id:
                try:
                    channel = self.client.get_channel((messages_id.get(i))["channel_id"])
                    msg = await channel.fetch_message((messages_id.get(i))["message_id"])
                    await msg.edit(embed=self.set_embed(i))
                except Exception:
                    pass



class EVENT_refresh(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.event = Listener(self.client) 

        # self.refresh.start()


    def cog_unload(self):
        self.refresh.cancel()


    @commands.Cog.listener()
    async def on_ready(self):
        __import__("is_ready").Is_Ready().event("refresh")


    seconds = (json.load(open("./config/config.json")))["refresh_time"]
    @tasks.loop(seconds=seconds)
    async def refresh(self):
        try:
            await self.event.connect()
            await self.event.refresh()
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


    # options = [
    #     {
    #         "name":"type",
    #         "description":"Type d'alliance",
    #         "required":True,
    #         "type":3,
    #         "choices":[
    #             {
    #                 "name": "Batiment Planetaire",
    #                 "value": "batiment_planetaire"
    #             },
    #             {
    #                 "name": "Batiment Lunaire",
    #                 "value": "batiment_lunaire"
    #             },
    #             {
    #                 "name": "Recherches",
    #                 "value": "recherches"
    #             },
    #             {
    #                 "name": "Vaisseaux Militaires",
    #                 "value": "vaisseaux_militaires"
    #             },
    #             {
    #                 "name": "Vaisseaux Civils",
    #                 "value": "vaisseaux_civils"
    #             },
    #             {
    #                 "name": "Défense Planetaire",
    #                 "value": "defense_planetaire"
    #             },
    #             {
    #                 "name": "Défense Lunaire",
    #                 "value": "defense_lunaire"
    #             }]
    #     }
    # ]
    # @cog_ext.cog_slash(name="get", description="Obtenir les informations des alliances", guild_ids=[805927681031405578], options=options)
    # async def get(self, ctx:SlashContext, type):
    #     await self.event.connect()
    #     await self.event.send(ctx, type)
    async def type_autocomplete(self, interaction: discord.Interaction, current: str):
        record_names = ["Batiment Planetaire", "Batiment Lunaire", "Recherches", "Vaisseaux Militaires", "Vaisseaux Civils", "Défense Planetaire", "Défense Lunaire"]
        record_values = ["batiment_planetaire", "batiment_lunaire", "recherches", "vaisseaux_militaires", "vaisseaux_civils", "defense_planetaire", "defense_lunaire"]
        return [
            app_commands.Choice(name=record_names[i], value=record_values[i])
            for i in range(len(record_names))
        ]

    @app_commands.command()
    @app_commands.autocomplete(type=type_autocomplete)
    async def send(self, ctx: discord.Interaction, type: str):        
        await self.event.connect()
        if type == "all":
            await self.event.send(ctx, "batiment_planetaire")
            await self.event.send(ctx, "batiment_lunaire")
            await self.event.send(ctx, "recherches")
            await self.event.send(ctx, "vaisseaux_militaires")
            await self.event.send(ctx, "vaisseaux_civils")
            await self.event.send(ctx, "defense_planetaire")
            await self.event.send(ctx, "defense_lunaire")
        else:
            await self.event.send(ctx, type)






async def setup(client):
    await client.add_cog(EVENT_refresh(client))
