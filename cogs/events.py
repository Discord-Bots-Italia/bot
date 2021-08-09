import discord, config, asyncio
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = member.guild.get_role(config.bot_role)
        if member.bot:
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return
        guild_id = payload.guild_id
        user_id = payload.user_id
        emoji = payload.emoji
        channel_id = payload.channel_id
        message_id = payload.message_id
        ch = self.bot.get_channel(channel_id)
        channel = self.bot.get_channel(config.logs_channel)
        if guild_id == config.dbi_verification:
            if channel_id == config.verification_channel:
                message = await ch.fetch_message(message_id)
                nomebot = message.embeds[0].title
                autore = message.embeds[0].footer.text
                if emoji.name == '✅':
                    emb = discord.Embed(description = f'✅ | {nomebot} di <@{autore}> è stato approvato da <@{user_id}>', colour = discord.Colour.green())
                    app = await channel.send(content = f'<@{autore}>', embed=emb)

                    jump = discord.Embed(description=f'[Link]({app.jump_url})')
                    await ch.send(embed=jump)
                    await message.clear_reactions()

                if emoji.name == "❎":
                    def check(m):
                        return m.author.id == user_id and m.channel == ch

                    try:
                        await ch.send('Ragione?')
                        ms = await self.bot.wait_for("message",check=check,timeout=60)

                    except asyncio.TimeoutError:
                        h = await ch.send("Timed out.")
                        await asyncio.sleep(5)
                        return await h.delete()

                    embed = discord.Embed(title="Bot Rifiutato",description=f"❌ | {nomebot} di <@{autore}> è stato rifiutato da <@{user_id}>",colour=discord.Colour.red())
                    embed.add_field(name="Ragione",value=ms.content)
                    rej = await channel.send(content=f"<@{autore}>",embed=embed)

                    jump = discord.Embed(description=f'[Link]({rej.jump_url})')
                    await ch.send(embed=jump)

                    await message.clear_reactions()

def setup(bot):
    bot.add_cog(Events(bot))
