from lib2to3.pgen2.token import DOUBLESLASH
import discord
from discord.ext import commands
from discord.ui import View, Modal
from datetime import *
import os
import myConfig

bg_failGuildId = myConfig.bg_failGuildId
debugGuildId = myConfig.debugGuildId
joinChannelId = myConfig.joinChannelId
memberCountChannelId = myConfig.memberCountChannelId
botCountChannelId = myConfig.botCountChannelId
userCountChannelId = myConfig.userCountChannelId
joinRoleId = myConfig.joinRoleId
suggestionChannelIds = myConfig.suggestionChannelIds
pollChannelIds = myConfig.pollChannelIds
token = myConfig.token


class MainBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned_or("$"), intents=intents)

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

async def updateStats():
  statsChannel = bot.get_channel(memberCountChannelId)
  userChannel = bot.get_channel(userCountChannelId)
  botChannel = bot.get_channel(botCountChannelId)
  memberCount = bot.get_guild(bg_failGuildId).member_count
  botCount = 0
  members = bot.get_guild(bg_failGuildId).members
  for user in members:
    if user.bot:
      botCount += 1
  await statsChannel.edit(name = f"Member count: {memberCount}")
  await botChannel.edit(name = f"Bot count: {botCount}")
  await userChannel.edit(name = f"User count: {memberCount - botCount}")

bot = MainBot()

async def fetchYesChannelId():
  for id in myConfig.approvedChannel:
    channel = bot.get_channel(id)
    if channel is not None:
      return channel

async def fetchNoChannelId():
  for id in myConfig.rejectedChannel:
    channel = bot.get_channel(id)
    if channel is not None:
      return channel

async def mostReaction(message):
  mostEmoji = None
  mostCount = 0
  for reaction in message.reactions:
    count = reaction.count
    if count > mostCount:
      mostCount = count
      mostEmoji = reaction.emoji
  return mostEmoji




async def suggestionsAction(payload, message, user):
  if str(payload.emoji) == "⭐":
    approvedChannel = await fetchYesChannelId()
    await message.delete()
    newEmbed = message.embeds[0]
    newEmbed.colour = discord.Colour.gold()
    newEmbed.set_footer(text=f"Прието от: {user}")
    newEmbed.timestamp = discord.Embed.Empty
    await approvedChannel.send(embed = newEmbed)
    return
  elif str(payload.emoji) == "⛔":
    rejectedChannel = await fetchNoChannelId()
    await message.delete()
    newEmbed = message.embeds[0]
    newEmbed.colour = discord.Colour.red()
    newEmbed.set_footer(text=f"Отказано от: {user}")
    newEmbed.timestamp = discord.Embed.Empty
    await rejectedChannel.send(embed = newEmbed)
    return

async def pollsAction(payload, message, user):
  newEmbed = message.embeds[0]
  newEmbed.timestamp = datetime.now()

  if str(payload.emoji) == "⭐":
    await message.delete()
    approvedChannel = await fetchYesChannelId()
    newEmbed.colour = discord.Colour.gold()
    emoji = await mostReaction(message)
    newEmbed.title = f"Приетата опция е: {emoji}"
    newEmbed.set_footer(text=f"Прието")
    await approvedChannel.send(embed = newEmbed)
    return


  elif str(payload.emoji) == "⛔":
    await message.delete()
    rejectedChannel = await fetchNoChannelId()
    newEmbed.colour = discord.Colour.red()
    newEmbed.title = f"Отказано от: {user}"
    newEmbed.set_footer(text=f"Отказано")
    await rejectedChannel.send(embed = newEmbed)
    return

#See all extensions
@bot.slash_command(name="listcogs", description="Lists all extensions", guild=discord.Object(id=debugGuildId))
async def slef(ctx):
  list = []
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      list.append(filename[:-3])
  await ctx.respond(f"{list}", ephemeral = True)

#Load extensions
@bot.slash_command(name="loadcog", description="Loads cog", guild=discord.Object(id=debugGuildId))
async def sfwe(ctx, name:str):
    bot.load_extension(f"cogs.{name}")
    await ctx.respond("Done", ephemeral=True)

#Unloads extensions
@bot.slash_command(name="unloadcog", description="Unloads cog", guild=discord.Object(id=debugGuildId))
async def sfwe(ctx, name:str):
    bot.unload_extension(f"cogs.{name}")
    await ctx.respond("Done", ephemeral=True)

#Shows user information
@bot.slash_command(name="userinfo", description="Gets info about a user.")
async def info(ctx: discord.ApplicationContext, user: discord.Member = None):
    user = user or ctx.author  # If no user is provided it'll use the author of the message
    embed = discord.Embed(
        fields=[
            discord.EmbedField(name="ID", value=str(user.id), inline=False),  # User ID
            discord.EmbedField(
                name="Created",
                value=discord.utils.format_dt(user.created_at, "F"),
                inline=False,
            ),  # When the user's account was created
        ],
    )
    embed.set_author(name=user.name)
    embed.set_thumbnail(url=user.display_avatar.url)

    if user.colour.value:  # If user has a role with a color
        embed.colour = user.colour

    if isinstance(user, discord.User):  # Checks if the user in the server
        embed.set_footer(text="This user is not in this server.")
    else:  # We end up here if the user is a discord.Member object
        embed.add_field(
            name="Joined",
            value=discord.utils.format_dt(user.joined_at, "F"),
            inline=False,
        )  # When the user joined the server

    await ctx.respond(embeds=[embed])  # Sends the embed
    
#No more than 1 reaction
@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
  done = False
  channel = bot.get_channel(payload.channel_id)
  message = await channel.fetch_message(payload.message_id)
  user = await bot.get_or_fetch_user(payload.user_id)
  if payload.channel_id in suggestionChannelIds or payload.channel_id in pollChannelIds:
    print(str(payload.emoji))
    if payload.user_id == 878274765624848424:
      if str(payload.emoji) == "🗑️":
        await message.delete()
        done = True
      if channel.id in suggestionChannelIds:
        await suggestionsAction(payload, message, user)
        done = True
      elif channel.id in pollChannelIds:
        await pollsAction(payload, message, user)
        done = True
    if done == False:
      for reaction1 in message.reactions:
        users = [user async for user in reaction1.users()]
        if payload.member in users and not payload.member.bot and str(payload.emoji) != str(reaction1.emoji):
          await message.remove_reaction(reaction1.emoji, payload.member)

#Reloads the stats
@bot.slash_command(name="reloadstats", description="Reloads the stats")
async def reload(ctx):
  await updateStats()
  await ctx.respond("Done!", ephemeral = True)

#Join and leave updateStats()
@bot.event
async def on_member_join(member: discord.Member):
  await updateStats()
@bot.event
async def on_member_remove(member: discord.Member):
  await updateStats()

#Loads all extensions
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')
   
#To hide the token
bot.run(token)