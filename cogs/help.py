import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        __import__("is_ready").Is_Ready().command("help")

    
    # @cog_ext.cog_slash(name="help", description="Permet d'avoir la liste des commandes", guild_ids=[799356517962874880])
    @commands.hybrid_command(name="help", description="Permet d'avoir la liste des commandes")
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(
            title = "Liste des commandes",
            colour = discord.Colour.random()
        )
        embed.add_field(name="`/config`", value="Permet d'afficher la liste des configurations", inline=False)
        embed.add_field(name="`/send <type>`", value="Permet d'envoyer un type d'alliance afin qu'il soit actualisé par la suite\n**__type__**:\n- `all`\n- `batiment_planetaire`\n- `batiment_lunaire`\n- `recherches`\n- `vaisseaux_militaires`\n- `vaisseaux_civils`\n- `defense_planetaire`\n- `defense_lunaire`", inline=False)
        embed.add_field(name="`/load`", value="Charger une extension", inline=False)
        embed.add_field(name="`/unload`", value="Décharger une extension", inline=False)
        embed.add_field(name="`/reload`", value="Reharger une extension", inline=False)
        embed.add_field(name="`/cogs`", value="Affiche la liste des extensions et leurs état", inline=False)
        # embed.add_field(name="`/setprefix <prefixe>`", value="Permet de modifier pour soit le prefixe du bot lors de l'utilisation d'une commande ***(Cooldown de 2min)***", inline=False)
        embed.set_footer(text="Demandé par " + ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        


async def setup(client):
    await client.add_cog(Help(client))
