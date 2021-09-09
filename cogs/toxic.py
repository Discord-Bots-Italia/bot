import discord, config
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

class Toxic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.toxic_words = ['dc,da', 'dc;da', 'dc , da', "che me ne fot", "chi te l'ha chiesto", "cazzo che me ne frega", "who asked", "dc da", "da dc", "don't care", "didn't ask", "dc, da", "dc ,da", "dc; da", "dc ;da", "che me ne frega", "https://tenor.com/view/the-vasteness-i-dont-give-a-shit-gif-12319215", "https://tenor.com/view/ea-me-che-me-ne-fott-gif-21398276", "https://tenor.com/view/che-me-ne-fott-gif-22944800", "stay mad", "cry about", "shut up", "cope"]
    
    async def toxic_check(self, message):
        if message.guild.id == config.dbi:
            if message.author.bot:
                return 

            check = False

            for x in self.toxic_words:
                if x.lower() in message.content.lower():
                    check = True
                    break
            
            if check:
                points = await (await self.bot.db.execute("SELECT points FROM toxic WHERE user=?", (message.author.id,))).fetchone()
                if points:
                    await self.bot.db.execute("UPDATE toxic SET points=? WHERE user=?", (points[0]+1, message.author.id))
                else:
                    await self.bot.db.execute("INSERT INTO toxic (user, points) VALUES (?, ?)", (message.author.id, 1))
                await self.bot.db.commit()
                await message.reply("`+1` toxic point, godo")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.toxic_check(after)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.toxic_check(message)

    @cog_ext.cog_slash(guild_ids=[config.dbi], name="toxic", description="Quanti punti toxic hai?", options=[
        create_option(
            name="membro",
            description="Membro",
            option_type=6,
            required=False
        )
     ])
    async def toxic_slash(self, ctx: SlashContext, membro=None):
        await self.toxic(ctx, membro)

    @commands.command()
    async def toxic(self, ctx, member: discord.Member=None):
        "Quanti punti toxic hai?"

        member = member or ctx.author
        points = await (await self.bot.db.execute("SELECT points FROM toxic WHERE user=?", (member.id,))).fetchone()
        points = 0 if not points else points[0]

        if points == 1:
            word = "point"
        else:
            word = "points"

        try: await ctx.reply(f"**{str(member)}**: `{points}` toxic {word}, e si gode", mention_author=False)
        except: await ctx.send(f"**{str(member)}**: `{points}` toxic {word}, e si gode")

    @cog_ext.cog_slash(guild_ids=[config.dbi], name="leaderbord", description="Chi è il piú toxic?")
    async def leadeboard_slash(self, ctx: SlashContext):
        await self.leaderboard(ctx)

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx):
        "Chi è il piú toxic?"

        users = {}
        data = await (await self.bot.db.execute("SELECT * FROM toxic")).fetchall()
        for x in data:
            users[int(x[0])] = int(x[1])

        if len(users) == 0:
            try: await ctx.reply("Niente toxic, non godo", mention_author=False)
            except: await ctx.send("Niente toxic, non godo")
            return

        res = ""
        lb = sorted(users, key=lambda x : users[x], reverse=True)
        count = 0
        for x in lb:
            count += 1
            if count > 20:
                break
            u = self.bot.get_user(x)
            if not u:
                u = await self.bot.fetch_user(x)
            word = "point" if users[x] == 1 else "points"
            res += f"`{count}.` **{str(u)}**: `{users[x]}` {word}\n"

        try: await ctx.reply(res, mention_author=False)
        except: await ctx.send(res, hidden=True)
            
def setup(bot):
    bot.add_cog(Toxic(bot))
