import discord
import os, pathlib, subprocess, time
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
dire = os.path.dirname(__file__)

def get_path(path):
    if os.path.isabs(path):
        return os.path.abspath(path)
    return os.path.abspath(os.path.join(dire, path))


@bot.command()
async def imgview(ctx, img):
    global dire

    path = get_path(img)

    if img.lower().endswith((".png", ".jpg", ".gif")) and pathlib.Path(path).is_file():
        await ctx.send(file=discord.File(path))
    else:
        await ctx.send("not an image file")


@bot.command()
async def imgall(ctx):
    global dire

    items = os.listdir(dire)

    for i in items:
        path = get_path(i)

        if i.lower().endswith((".png", ".jpg", ".gif")):
            await ctx.send(file=discord.File(path))
            print("done")
        else:
            print("problem")


@bot.command()
async def ls(ctx):
    global dire

    items = os.listdir(dire)
    message = ""

    if len(items) == 1:
        message = f"**-** {items[0]}\n"

    else:
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

    new_dir = get_path(arg)

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

    path = get_path(name)

    if os.path.exists(path):
        await ctx.send("directory already exists")

    else:
        os.makedirs(path)
        await ctx.send("directory created")


@bot.command()
async def rmdir(ctx, name):

    path = get_path(name)

    if not os.path.isdir(path):
        await ctx.send("directory doesn't exist")
        return

    if os.listdir(path):
        await ctx.send("directory is not empty")

    else:
        os.rmdir(path)
        await ctx.send("directory removed")


@bot.command()
async def getfile(ctx, name):
    path = get_path(name)

    if os.path.isfile(path):
        await ctx.send("getting file")
        time.sleep(0.2)
        await ctx.send(file=discord.File(path))

    else:
        await ctx.send("file doesn't exist")


@bot.command()
async def rm(ctx, name):
    path = get_path(name)

    if os.path.isfile(path):
        os.remove(path)
        await ctx.send("file removed")

    else:
        await ctx.send("file doesn't exist")

bot.run('Your discord bot token here')
