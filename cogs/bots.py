import discord, config
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

class Bots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(guild_ids=[config.dbi], name="submit", description="Invia una richiesta per aggiungere il tuo bot nel server.", options=[
        create_option(
            name="nome",
            description="Nome del bot",
            option_type=3,
            required=True
        ), create_option(
            name="id",
            description="ID del bot",
            option_type=6,
            required=True
        ), create_option(
            name="libreria",
            description="Libreria usata per sviluppare il bot",
            option_type=3,
            required=True,
            choices=[
                  create_choice(
                    name="discord.py",
                    value="discord.py"
                  ),
                  create_choice(
                    name="discord.js",
                    value="discord.js"
                  ),
                  create_choice(
                    name="discordgo",
                    value="discordgo"
                  ), create_choice(
                    name="discordia",
                    value="discordia"
                  ), create_choice(
                    name="JDA",
                    value="JDA"
                  ), create_choice(
                    name="Discord4J",
                    value="Discord4J"
                  ), create_choice(
                    name="Discord.Net",
                    value="Discord.Net"
                  )
                ]
        ), create_option(
            name="prefisso",
            description="Prefisso del bot",
            option_type=3,
            required=True
        ), create_option(
            name="versione",
            description="Versione del bot",
            option_type=3,
            required=False,
            choices=[
                  create_choice(
                    name="Alpha",
                    value="Alpha"
                  ), create_choice(
                    name="Beta",
                    value="Beta"
                  ), create_choice(
                    name="Stable",
                    value="Stable"
                  )
                ]
        ), create_option(
            name="sito",
            description="Sito web del bot",
            option_type=3,
            required=False
        )
     ])
    async def submit(self, ctx: SlashContext, nome: str, id, libreria: str, prefisso: str, versione: str = None, sito: str = None):
        "Invia una richiesta per aggiungere il tuo bot nel server."

        try:
            invito = discord.utils.oauth_url(int(id), permissions=discord.Permissions(0))
        except:
            invito = discord.utils.oauth_url(id.id, permissions=discord.Permissions(0))
        emb = discord.Embed(title=nome)
        if versione:
            emb.add_field(name="Versione", value=versione)

        emb.add_field(name="Invito", value=f'[Invito]({invito})')
        emb.add_field(name="Libreria", value=libreria)
        emb.add_field(name="Prefisso", value=prefisso)
        if sito:
            emb.add_field(name="Sito", value=sito)

        queue = self.bot.get_channel(config.queue_channel)
        verification = self.bot.get_channel(config.verification_channel)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        emb.set_thumbnail(url=ctx.author.avatar_url)
        emb.set_footer(text = ctx.author.id)

        msg = await queue.send(embed=emb)
        log = await verification.send(embed=emb)

        await log.add_reaction('✅')
        await log.add_reaction('❎')

        await ctx.send(embed=discord.Embed(description=f"[Inviato]({msg.jump_url}) {config.success}!", colour=discord.Colour.blurple()))

def setup(bot):
    bot.add_cog(Bots(bot))
