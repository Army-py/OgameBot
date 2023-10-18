from discord.ext import commands


class Listener(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        __import__("is_ready").Is_Ready().event("error")


    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandNotFound):
            # await ctx.send('Command invalide ! `s!help`', delete_after=5)
            # await ctx.message.delete()
            pass
        if isinstance(error, commands.CommandOnCooldown):
            heure = int((error.retry_after / 3600))
            minute = int((error.retry_after - (3600 * heure)) / 60)
            secondes = int(error.retry_after - (3600 * heure) - (60 * minute))
            await ctx.send(f"{ctx.author.mention} tu as déjà fait la commande récemment, réessaye dans **{heure}h {minute}min {secondes}s**")
            await ctx.message.delete()
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention} tu n'as pas la permission d'utiliser cette commande")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send(f"{error}")
        if isinstance(error, (commands.BadArgument, commands.BadUnionArgument)):
            await ctx.message.delete()
            await ctx.send(error)
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"{ctx.author.mention} tu n'as pas la permission d'utiliser cette commande")
        if isinstance(error, commands.MissingAnyRole):
            #await ctx.send(error, delete_after=5)
            await ctx.send("**Tu n'as pas les rôles nécessaires pour exécuter cette commande :** " + f"{error.missing_roles}".translate({ord(i): None for i in "()'"}))
        if isinstance(error, commands.NotOwner):
            await ctx.send(f"{ctx.author.display_name} tu n'es pas accès à cette commande")
            await ctx.message.delete()



async def setup(client):
    await client.add_cog(Listener(client))