import logging
import os
from pathlib import Path

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    allowed_mentions=discord.AllowedMentions.none(),
)

dire = Path(__file__).resolve().parent
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}


def get_path(value):
    path = Path(value).expanduser()

    if not path.is_absolute():
        path = dire / path

    return path.resolve()


async def send_text(ctx, text):
    for start in range(0, len(text), 1900):
        await ctx.send(text[start:start + 1900])


@bot.check
async def owner_only(ctx):
    return await bot.is_owner(ctx.author)


@bot.command()
async def imgview(ctx, *, img):
    path = get_path(img)

    if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
        await ctx.send("Not a supported image file.")
        return

    with discord.File(path) as attachment:
        await ctx.send(file=attachment)


@bot.command()
async def imgall(ctx):
    # Collect paths before awaiting, so a later cd cannot change this listing.
    images = [
        path
        for path in sorted(dire.iterdir())
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]

    if not images:
        await ctx.send("No supported images in this directory.")
        return

    for path in images:
        with discord.File(path) as attachment:
            await ctx.send(file=attachment)


@bot.command()
async def ls(ctx):
    items = sorted(path.name for path in dire.iterdir())

    if not items:
        await ctx.send("Directory is empty.")
        return

    if len(items) == 1:
        message = f"- {items[0]}"
    else:
        lines = []

        for index, item in enumerate(items):
            if index == 0:
                prefix = "┌"
            elif index == len(items) - 1:
                prefix = "└"
            else:
                prefix = "├"

            lines.append(f"{prefix} {item}")

        message = "\n".join(lines)

    await send_text(ctx, message)


@bot.command()
async def cd(ctx, *, arg):
    global dire

    new_dir = get_path(arg)

    if not new_dir.is_dir():
        await ctx.send("Directory doesn't exist.")
        return

    dire = new_dir
    await send_text(ctx, str(dire))


@bot.command()
async def pwd(ctx):
    await send_text(ctx, str(dire))


@bot.command()
async def mkdir(ctx, *, name):
    path = get_path(name)

    try:
        path.mkdir(parents=True)
    except FileExistsError:
        await ctx.send("A file or directory already exists at that path.")
        return

    await ctx.send("Directory created.")


@bot.command()
async def rmdir(ctx, *, name):
    path = get_path(name)

    if not path.is_dir():
        await ctx.send("Directory doesn't exist.")
        return

    if any(path.iterdir()):
        await ctx.send("Directory is not empty.")
        return

    # rmdir also refuses nonempty directories if their contents change.
    path.rmdir()
    await ctx.send("Directory removed.")


@bot.command()
async def getfile(ctx, *, name):
    path = get_path(name)

    if not path.is_file():
        await ctx.send("File doesn't exist.")
        return

    with discord.File(path) as attachment:
        await ctx.send(file=attachment)


@bot.command()
async def rm(ctx, *, name):
    path = get_path(name)

    if not path.is_file():
        await ctx.send("File doesn't exist.")
        return

    path.unlink()
    await ctx.send("File removed.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.CheckFailure):
        await ctx.send("Only the bot owner can use these commands.")
        return

    if isinstance(error, commands.UserInputError):
        await ctx.send(f"Invalid or missing argument. Try !help {ctx.command}")
        return

    original = getattr(error, "original", error)

    if isinstance(original, OSError):
        await send_text(ctx, f"Filesystem error: {original}")
        return

    if isinstance(original, discord.HTTPException):
        logging.warning("Discord request failed: %s", original)
        try:
            await ctx.send(
                "Discord couldn't complete the request. "
                "Check the file size and bot permissions."
            )
        except discord.HTTPException:
            pass
        return

    raise error


bot.run(os.environ["DISCORD_BOT_TOKEN"])
