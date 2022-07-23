from config import *
import discord
from discord.ext import commands
import requests
from uuid import uuid4
from nudenet import NudeClassifier
from discord_webhook import DiscordWebhook

intent = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intent, help_command=None)
classifier = NudeClassifier()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    allowedimages = ['jpg', 'jpeg', 'png']
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.split('.')[-1] in allowedimages:

                isitsafe = await issafeimage(attachment.url)
                if isitsafe["safe"]:
#                    await message.channel.send("This image is safe")
                    pass
                else:
                    await message.delete()
                    await message.channel.send(f"This image has the horny so i censored it for you <@{message.author.id}>", file=discord.File(isitsafe["path"]))
                    
async def download_image(url):
    SEND = url
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/996330339460976700/37boOM2O3Ylvhs20geu3HUc4s5pbByagaD9JycOdMvb0PBu2wpDvKs7G1t-8UTZ8zk7X', username="Images", rate_limit_retry=True, content=SEND)
    webhook.execute()
    gg = requests.get(url)
    path = 'images/' + "SPOILER_"+str(uuid4()) + '.jpg'
    with open(path, 'wb') as f:
        f.write(gg.content)
    return path

async def issafeimage(url):
    path = await download_image(url)
    print(path)
    nude = classifier.classify(path)
    print(nude)
    print(nude[path]["unsafe"])
    if nude[path]["unsafe"] >= 0.75:
        return {"safe": False, "path": path}
    else:
        return {"safe": True, "path": path}

@bot.command()
async def help(ctx):
    await ctx.send("""```
!help - shows this message

About the nude classifier: this bot uses a neural network to detect if the image is lewd or not. The neural network is old so it gives alot of fals positives. if you know any better ways of detecting if the image is safe or not, please let me know.
Invite link: https://discord.com/api/oauth2/authorize?client_id=996310963710075011&permissions=8&scope=bot
Made by: NullRien#9999
```
    """)

bot.run(DISCORDTOKEN)