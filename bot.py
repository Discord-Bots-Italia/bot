import discord
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix='>', owner_ids = [488398758812319745, 446650423416193034],owner_id=None)
bot.remove_command('help')

@bot.event
async def on_ready():
   
    print("I'm Online! \nName:", bot.user, '\nID:', bot.user.id)
   
    await bot.change_presence(activity = discord.Streaming(name='Checking the queue', url = 'https://www.twitch.tv/ssebordd'))
@bot.command()
@commands.has_permissions(administrator=True, kick_members=True)
async def clear(ctx, amount=100):
  """Delete some messages"""
  await ctx.message.delete()
  await ctx.channel.purge(limit=amount)   
@bot.command()
async def submit(ctx):
    embed = discord.Embed(colour=ctx.author.colour)
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        await ctx.send('Come si chiama il tuo bot?')      
        mx = await bot.wait_for("message",check=check,timeout=60)
        embed.title = mx.content    
    except asyncio.TimeoutError:
        return await ctx.send(f"{ctx.author.mention} tempo scaduto :clock:!")
    try:
        await ctx.send("Qual è la versione del tuo bot?")
        mx = await bot.wait_for("message",check=check,timeout=60)
        embed.add_field(name="Versione",value=mx.content)
    except asyncio.TimeoutError:
        return await ctx.send(f"{ctx.author.mention} tempo scaduto :clock:!")
    try:
        await ctx.send("Manda il client id del tuo bot")
        mx = await bot.wait_for("message",check=check,timeout=60)
        try:
            int(mx.content)
        except:
            return await ctx.send("Client id non valido")
        invito = discord.utils.oauth_url(int(mx.content),permissions=discord.Permissions(0))
        embed.add_field(name="Invito",value=f'[Invito]({invito})')
    except asyncio.TimeoutError:
        return await ctx.send(f"{ctx.author.mention} tempo scaduto :clock:!")
    try:
        await ctx.send("Qual è la libreria che usi per il tuo bot?")
        mx = await bot.wait_for("message",check=check,timeout=60)
        embed.add_field(name="Libreria",value=mx.content)
    except asyncio.TimeoutError:
        return await ctx.send(f"{ctx.author.mention} tempo scaduto :clock:!")
    try:
        await ctx.send("Qual è il prefisso")
        mx = await bot.wait_for("message",check=check,timeout=60)
        embed.add_field(name="Prefisso",value=mx.content)
    except asyncio.TimeoutError:
        return await ctx.send(f"{ctx.author.mention} tempo scaduto :clock:!")
    try:
        await ctx.send("Manda il sito del tuo bot. Se non lo hai rispondi `no`")
        mx = await bot.wait_for("message",check=check,timeout=60)
        if not mx.content == "no":
            embed.add_field(name="Website",value=mx.content)
    except asyncio.TimeoutError:
        return await ctx.send(f"{ctx.author.mention} tempo scaduto :clock:!")
    channel = bot.get_channel(616071707178041364)
    ch = bot.get_channel(615485726775050242)
    embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text = ctx.author.id)
   
    msg = await channel.send(embed=embed)
    log = await ch.send(embed=embed)
   
    hm = discord.Embed(description=f'[Link]({msg.jump_url})')
   
    await ctx.send(content='Inviato!', embed=hm)
    
    await log.add_reaction('✅')
    await log.add_reaction('❎')
   
@submit.error
async def on_submit_error(ctx, error):
    print(error)
    await ctx.author.send(error)
    await ctx.message.delete()
 
   
@bot.command()
async def help(ctx):
   
    emb = discord.Embed(description='''Invia il tuo Bot in questo server, per aggiungerlo alla coda usa 
`>submit`''', colour = ctx.author.colour)
    emb.set_thumbnail(url=bot.user.avatar_url) 
    await ctx.send(embed=emb)
    
@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return
    guild_id = payload.guild_id
    user_id = payload.user_id
    emoji = payload.emoji
    channel_id = payload.channel_id
    message_id = payload.message_id
    ch = bot.get_channel(channel_id)
    channel = bot.get_channel(615503696666689536)
    if guild_id == 607040653733527564:
        
        if channel_id == 615485726775050242:

            message = await ch.fetch_message(message_id)
            nomebot = message.embeds[0].title
            autore = message.embeds[0].footer.text
            if emoji.name == '✅':
                emb = discord.Embed(title='Bot Approvato', description = f'{nomebot} di <@{autore}> è stato approvato da <@{user_id}>', colour = 0xffffff)
                app = await channel.send(content = f'<@{autore}>', embed=emb)
                
                jump = discord.Embed(description=f'[Link]({app.jump_url})')
                await ch.send(embed=jump)
                await message.clear_reactions()
            
            if emoji.name == "❎":
                
                def check(m):
                    
                    return m.author.id == user_id and m.channel == ch
                
                try:
                    
                    await ch.send('Ragione?')
                    ms = await bot.wait_for("message",check=check,timeout=60)
                
                except asyncio.TimeoutError:
                    h = await ch.send("Timed out.")
                    await asyncio.sleep(5)
                    await ms.delete()
                    return await h.delete()

                     
                embed = discord.Embed(title="Bot Rifiutato",description=f"{nomebot} di <@{autore}> è stato rifiutato da <@{user_id}>",colour=discord.Colour.red())
                embed.add_field(name="Ragione",value=ms.content)
                rej = await channel.send(embed=embed)
                
                jump = discord.Embed(description=f'[Link]({rej.jump_url})')
                await ch.send(embed=jump)
                
                await message.clear_reactions()
                
@bot.command()
async def ping(ctx):
    
    pong = (round(bot.latency * 1000))
    
    emb = discord.Embed(description = f':ping_pong:{pong}ms', colour = ctx.author.colour)
    emb.set_author(name = f'{ctx.author.name} Pong!', icon_url = ctx.author.avatar_url)
    
    await ctx.send(embed = emb)
    

@bot.event
async def on_member_join(member):
    
    guild = member.guild 
    
    role = guild.get_role(611324610184609853)
    
    if member.bot:
        
        await member.add_roles(role)

bot.run('NjA3MDQwNzk2NzgwMTM0NDIy.XW4u-g.01H7jCK2wIDzjaVTrqK-P83Weqc')
