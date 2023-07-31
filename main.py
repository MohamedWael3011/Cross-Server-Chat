import discord
from discord import webhook
from discord.ext import commands
import os
import aiohttp
import traceback
from dotenv import load_dotenv
intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)
load_dotenv()


ChannelName = "flow-latino"
@client.event
async def on_ready():
    print('Flow Latino is running! Currently serving {0.user}'.format(client))
    await client.tree.sync()
  
@client.event
async def on_guild_join(guild):
    # Loop through the text channels in the guild
    for channel in guild.text_channels:
        if channel.name == ChannelName:
            return
    await guild.create_text_channel(ChannelName)
  





@client.event
async def on_message(message):
    if message.channel.name == ChannelName:
        if not (message.author.bot):
            await message.delete()
            # Get the user's nickname and profile picture URL
            WebHookName = str(message.author.display_name)
            WebHookURL = message.author.display_avatar.url
            async with aiohttp.ClientSession() as session:
                async with session.get(WebHookURL) as response:
                    WebHookPFP = await response.read()
            # Send the message to all the other servers
            for guild in client.guilds:
                channel = discord.utils.get(guild.text_channels, name=ChannelName)
                if channel:
                # Pass in the bot's username and avatar URL to the send() method
                    Webhook = await channel.create_webhook(name=WebHookName,avatar=WebHookPFP)
                    await Webhook.send(message.content,files= [await f.to_file() for f in message.attachments])
                    await Webhook.delete()


client.run(os.getenv('TOKEN'))

