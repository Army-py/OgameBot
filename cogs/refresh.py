import os
import pickle
from enum import Enum
import json

import discord
from discord.ext import commands, tasks
from discord_slash import SlashContext, cog_ext
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build


class ranges(Enum):
    batiment_planetaire = "A6:D21"
    batiment_lunaire = "A23:D30"
    recherches = "A32:D47"
    vaisseaux_militaires = "A49:D58"
    vaisseaux_civils = "A60:D65"
    defense_planetaire = "A67:D74"
    defense_lunaire = "A76:D81"


class Listener:
    def __init__(self, client):
        self.client = client
        self.SAMPLE_SPREADSHEET_ID_input = '1gW7Q4xEHGw_aSez9UuQCjG8CHoa3R0EGO2IWivp1720'


    def connect(self):
        creds = None
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    './bot config/credentials.json', SCOPES) # here enter the name of your downloaded JSON file
                creds = flow.run_local_server(port=48625)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
    
        service = build('sheets', 'v4', credentials=creds)
    
        # Call the Sheets API
        self.sheet = service.spreadsheets()


    def get_values(self, range):
        result_input = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID_input,
                            range=range).execute()
        values_input = result_input.get('values', [])
        return values_input


    def format_values(self, range):
        data = []
        for i in self.get_values(ranges[range].value):
            data.append(' - '.join([f"{lst}" for lst in i]))
        return data


    def get_color(self, range):
        file = open("./config/config.json")
        config = json.load(file)
        self.color = config[f"{range}.color"]
        file.close()


    def get_prefix(self, range):
        file = open("./config/config.json")
        config = json.load(file)
        self.color = config[f"{range}.prefix"]
        file.close()


    def set_embed(self, range):
        self.get_color(range)
        self.embed = discord.Embed(
            description = "```\n" + '\n'.join([f"{lst}" for lst in self.format_values(range)]) + "\n```",
            colour = discord.Colour.from_rgb(self.color[0], self.color[1], self.color[2])
        )
        return self.embed



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


    @tasks.loop(minutes=1.0)
    async def refresh(self):
        self.event.connect()
        print(self.event.get_values(ranges["batiment_planetaire"].value))


    options = [
        {
        "name":"type",
        "description":"Type d'alliance",
        "required":True,
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
        }
    ]
    # @commands.command()
    @cog_ext.cog_slash(name="get", description="Obtenir les informations des alliances", guild_ids=[805927681031405578], options=options)
    async def get(self, ctx:SlashContext, type):
        # await ctx.message.delete()
        
        self.event.connect()
        
        await ctx.send(embed=self.event.set_embed(type))


    @commands.command()
    async def send(self, ctx):
        await ctx.message.delete()
        
        self.event.connect()
        
        await ctx.send(embed=self.event.set_embed("batiment_planetaire"))





def setup(client):
    client.add_cog(EVENT_refresh(client))
