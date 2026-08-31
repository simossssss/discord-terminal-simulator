import discord
import os, pathlib,subprocess
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
dire = os.path.dirname(__file__)

@bot.command()
async def imgview(ctx, img):
        global dire
        
        if (img[-4:] == ".png" or img[-4:] == ".jpg" or img[-4:] == ".gif")and pathlib.Path(dire + "\\" + img).is_file():
            picture = discord.File(os.path.join(dire, img))
            await ctx.send(file=discord.File(dire+"\\"+img))
        
        else:
            await ctx.send("not an image file")

@bot.command()
async def imgall(ctx):
        global dire
        items = os.listdir(dire)

        for i in items:
            if i.lower().endswith((".png", ".jpg", ".gif")):
                await ctx.send(file=discord.File(dire+"\\"+i))
                print("done")
            else:
                print("problem")

@bot.command()
async def ls(ctx):
    global dire
    items = os.listdir(dire)
    message = ""

    for i, item in enumerate(items):
        if i == 0:
            message += f"┌ {item}\n"
        elif i == len(items) - 1:
            message += f"└ {item}\n"
        else:
            message += f"├ {item}\n"

    while message:
        await ctx.send(message[:1900])
        message = message[1900:]

@bot.command()
async def cd(ctx, arg):
    global dire

    new_dir = os.path.abspath(os.path.join(dire, arg))

    if not os.path.isdir(new_dir):
        await ctx.send("Invalid path name")

    else:
        dire = new_dir
        await ctx.send(dire)

@bot.command()
async def pwd(ctx):
    global dire
    await ctx.send(dire)

@bot.command()
async def mkdir(ctx, name):
    global dire
    items = os.listdir(dire)
    flag=False

    for i in items:
        if i == name:
            await ctx.send("directory already exists")
            flag=True
            break
    
    if flag==False:
        os.makedirs(dire+"\\"+name)
        await ctx.send("directory created")

@bot.command()
async def rmdir(ctx, name):
    global dire
    items = os.listdir(dire)

    if not items:
        flag=False
        for i in items:
            if i==name:
                flag=True
                os.rmdir(dire+"\\"+name)
                await ctx.send("directory removed")
                break
        if flag==False:
            await ctx.send("directory doesnt exists")

    else:
        await ctx.send("derectory is not empty")

bot.run('Your discord bot token here')
