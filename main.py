# Hello
import discord
from discord.ext import commands
import random
from threading import Thread
from flask import Flask
from datetime import datetime
import asyncio
import psutil
from xkcd import *
 
prefixes = ['x!', 'X!', 'sudo ', 'Sudo']
bot = commands.Bot(command_prefix = prefixes, case_insensitive = True)
bot.remove_command('help')

xkcdWebsiteURL = 'https://xkcd.com/'
CueBotTOPGGURL = 'https://top.gg/NOT_PUBLISHED_YET'

# bot keepAlive() script
app = Flask('')
@app.route('/')

def home():
    return f'================================================================================= <br>Discord Bot Name: {bot.user.name} <br>Hosting Platform: Repl.it <br>Bot Developer: Not Richard Nixon#5937<br>================================================================================='
 
def run():
  app.run(host = '0.0.0.0', port = 8080)
 
def keepAlive():
    t = Thread(target=run)
    t.start()

# bot on initialization
@bot.event
async def on_ready():
	
	bot.starttime = datetime.now()
	await bot.change_presence(status = discord.Status.online, activity = discord.Activity(type = discord.ActivityType.watching, name = f'{len(bot.users)} Users | x!help'))
	print(f'================================================================================= \nDiscord Bot Name: {bot.user.name} \nHosting Platform: Repl.it \nBot Developer: Not Richard Nixon#5937 \n================================================================================= \n\nBOT CONSOLE LOG BELOW: \n')

# on join server event
@bot.event
async def on_guild_join(guild):
	await bot.change_presence(status = discord.Status.dnd, activity = discord.Activity(type = discord.ActivityType.watching, name = f'{len(bot.users)} Users | x!help'))
	print('JOINED Server')

# on exit server event
@bot.event
async def on_guild_remove(guild):
	await bot.change_presence(status = discord.Status.dnd, activity = discord.Activity(type = discord.ActivityType.watching, name = f'{len(bot.users)} Users | x!help'))
	print('LEFT Server')

# on member join event
@bot.event
async def on_member_join(member):
	await bot.change_presence(status = discord.Status.dnd, activity = discord.Activity(type = discord.ActivityType.watching, name = f'{len(bot.users)} Users | x!help'))
	print(f'MEMBER Left Server ({member.guild.id} - {member.id}')

# on member exit event
@bot.event
async def on_member_remove(member):
	await bot.change_presence(status = discord.Status.dnd, activity = discord.Activity(type = discord.ActivityType.watching, name = f'{len(bot.users)} Users | x!help'))
	print(f'MEMBER Left Server ({member.guild.id} - {member.id}')

# xkcd command
@bot.command(aliases=['comic', 'sudo'])
async def xkcd(ctx, *, query = None):
	latest = getLatestComicNum()
	com = None
	rand = None

  # return comics
	if not query:
		com = Comic(latest)
	elif query.isdigit():
		try:
			com = Comic(query)
		except:
			await ctx.send(f'I couldn\'t find that. Make sure you give a number between 1 and {latest}')
	
	elif query.lower().startswith('r'):
		rand = random.randint(1, latest)
		com = Comic(rand)
	
	else:
		await ctx.send('I don\'t understand. Type "/help" for a list of commands.')
	
	if com:
		embed = discord.Embed(title = f'{com.getTitle()} (#`{rand if rand else query if query else latest}`)', description = com.getAltText(), color = 0xFFFFFE, timestamp = datetime.utcnow())
		embed.set_author(name = bot.user.name, url = xkcdWebsiteURL, icon_url = bot.user.avatar_url)
		embed.set_footer(text = f'Requested by {ctx.author}', icon_url = ctx.author.avatar_url)
		embed.set_image(url = com.getImageLink())
		await ctx.send(embed = embed)
    # await ctx.send(f'Number: {rand if rand else query if query else latest} \nTitle: {com.getTitle()} \nAlt Text: {com.getAltText()}')
    # await ctx.send(com.getImageLink())
	
	print('XKCD Command Called')

# explain commmand (Uses the getExplanation() feature from the xkcd python API. It's not perfect, but it's much better than trying to do it myself.)
@bot.command(aliases=['?', 'exp', 'explainxkcd'])
async def explain(ctx, *, query = None):
  latest = getLatestComicNum()

  if not query:
    await ctx.send(f'Here is the explaination for the latest comic, {latest} - "{Comic(latest).getTitle()}" \n{Comic(latest).getExplanation()}')

  elif query.isdigit():
    try:
      await ctx.send(f'Here is the explaination for {query} - "{Comic(query).getTitle()}" \n{Comic(query).getExplanation()}')
    except:
      await ctx.send(f'I couldn\'t find that. Make sure you give a number between 1 and {latest}')

  elif query.lower().startswith('r'):
    rand = random.randint(1, latest)
    await ctx.send(f'Here is the explanation for a random comic, {rand} - "{Comic(rand).getTitle()}" \n{Comic(rand).getExplanation()}')


  else:
    await ctx.send('I don\'t understand. Type "x!help" for a list of commands.')

  print('EXPLAIN Command Called')

# link command
@bot.command(aliases=['url'])
async def link(ctx, *, query = None):
  latest = getLatestComicNum()

  # return links
  if not query:
    await ctx.send(f'Here is the link to the latest comic, {latest} - "{Comic(latest).getTitle()}". \nhttps://www.xkcd.com/{latest}')

  elif query.isdigit():
    try:
      await ctx.send(f'Here is the link to {query} - "{Comic(query).getTitle()}" \nhttps://www.xkcd.com/{query}')
    except:
      await ctx.send(f'I couldn\'t find that. Make sure you give a number between 1 and {latest}')

  elif query.lower().startswith('r'):
    rand = random.randint(1, latest)
    await ctx.send(f'Here is the link to a random comic, {rand} - "{Comic(rand).getTitle()}" \nhttps://www.xkcd.com/{rand}')


  else:
    await ctx.send('I don\'t understand. Type "x!help" for a list of commands.')

  print('LINK Command Called')

# whatif command
@bot.command(aliases=['wif'])
async def whatif(ctx, *, query = None):
  latest = getLatestWhatIfNum()

  if not query:
    await ctx.send(f'Here is the latest What If? post, {latest} - "{getWhatIf(latest).getTitle()}" \n{getWhatIf(latest).getLink()}')

  elif query.isdigit():
    try:
      await ctx.send(f'Here is What If? #{query} - "{getWhatIf(query).getTitle()}" \n{getWhatIf(query).getLink()}')
    except:
      await ctx.send(f'I couldn\'t find that. Make sure you give a number between 1 and {latest}')

  elif query.lower().startswith('r'):
    rand = random.randint(1, latest)
    await ctx.send(f'Here is a random What If? article, {rand} - "{getWhatIf(rand).getTitle()}" \n{getWhatIf(rand).getLink()}')

  else:
    await ctx.send('I don\'t understand. Type "x!help" for a list of commands.')

  print('WHAT IF Command Called')

# bun command
@bot.command()
async def bun(ctx):
    await ctx.send('Command coming soon!')
    print('BUN Command Called')

# secret command
@bot.command()
async def secret(ctx):
    await ctx.send('This is not the secret command. Or is it?')
    print('SECRET Command Called')

# help command
@bot.command(aliases=['info'])
async def help(ctx):
	embed = discord.Embed(title = 'Help Page', color = 0xFFFFFE, timestamp = datetime.utcnow())
	embed.set_author(name = bot.user.name, url = xkcdWebsiteURL, icon_url = bot.user.avatar_url)
	embed.set_footer(text = f'Requested by {ctx.author}', icon_url = ctx.author.avatar_url)
	embed.set_thumbnail(url = bot.user.avatar_url)
	embed.add_field(name = 'Comic Related Stuff', value = 'The structure of a command is `x!<type> <argument>`. \n\n**Command Types:** \n`x!xkcd` (or `comic`) \nreturns an xkcd comic. \n`x!explain` (`?`, `exp`) \nreturns a link to the [explain xkcd wiki](https://www.explainxkcd.com/wiki/index.php/Main_Page). \n`x!link` (`url`)\nreturns a link to the [xkcd](https://xkcd.com/) site.\n`x!whatif` (`wif`)\nreturns a link to a [What If?](https://what-if.xkcd.com/) article. \n\n**Command Arguments:** \n•  `x!xkcd` (no argument) \nreturns the latest xkcd comic.\n• `x!xkcd 999` \nreturns xkcd 999.\n• `x!xkcd random` \nreturns a random xkcd.\n\nAll 3 arguments - empty, number, and random - work with the 4 command types above, giving 12 unique xkcd-related commands.\n', inline=False)
	embed.add_field(name = 'Other Stuff', value = '`x!help` (`x!info`)\nreturns this page \n`x!botinfo` (`x!binfo`)\nreturns info about the bot\n`x!ping` (`x!latency`)\nreturns the bot\'s latency and other statistics\n\n P.S. You can also write `sudo ` in place of `x!`', inline=False)
	await ctx.send(embed = embed)

	print('HELP COMMAND CALLED')

# botinfo command
@bot.command(aliases=['binfo'])
async def botinfo(ctx):
	embed = discord.Embed(title = 'Bot Info', color = 0xFFFFFE, timestamp = datetime.utcnow())
	embed.set_author(name = bot.user.name, url = xkcdWebsiteURL, icon_url = bot.user.avatar_url)
	embed.set_footer(text = f'Requested by {ctx.author}', icon_url = ctx.author.avatar_url)
	embed.set_thumbnail(url = bot.user.avatar_url)
	embed.add_field(name = 'Developer', value = 'Main: <@665633515756585031> (Owner)\nDesign: <@410590963379994639>', inline=False)
	embed.add_field(name = 'Language', value = 'Python and the [discord.py](https://discordpy.readthedocs.io/en/latest/) library', inline=False)
	embed.add_field(name = 'Hosting Platform', value = '[Repl.it](https://repl.it/)', inline=False)
	embed.add_field(name = 'Github Repository', value = '[Coming Soon](https://www.google.com/)', inline=False)
	
	await ctx.send(embed = embed)
	print('BOTINFO Command Called')

# ping command
@bot.command(aliases=['latency'])
async def ping(ctx):
	time = datetime.now() - bot.starttime
	days = time.days
	hours, remainder = divmod(time.seconds, 3600)
	minutes, seconds = divmod(remainder, 60)
	dunit = 'day' if days == 1 else 'days'
	hunit = 'hour' if hours == 1 else 'hours'
	munit = 'minute' if minutes == 1 else 'minutes'
	sunit = 'second' if seconds == 1 else 'seconds'
	

  

	embed = discord.Embed(title = '🏓 Pong!', color = 0xFFFFFE, timestamp = datetime.utcnow())
	embed.set_author(name = bot.user.name, url = xkcdWebsiteURL, icon_url = bot.user.avatar_url)
	embed.set_footer(text = f'Requested by {ctx.author}', icon_url = ctx.author.avatar_url)
	embed.add_field(name = ':signal_strength: Latency', value = (f'`{round(bot.latency * 1000)}`ms'), inline=True)
	embed.add_field(name = ':robot: Hardware', value = (f'Cores → `{psutil.cpu_count()}` \nCPU → `{round(psutil.cpu_percent())}`% \nRAM → `{round(psutil.virtual_memory()[2])}`%'), inline=True)
	embed.add_field(name = ':chart_with_upwards_trend: Uptime', value = (f'`{days}` {dunit} \n`{hours}` {hunit} \n`{minutes}` {munit} \n`{seconds}` {sunit}'), inline=True)
	await ctx.send(embed = embed)
	
	print('PING Command Called')

keepAlive()
infile = open('bot_token.txt', 'r')
TOKEN = infile.readline()
bot.run(TOKEN)