# alt-text cog for ERIS
# Written by Nate (@iNatie)
# Based off the discord.js bot written by 9vult
# A project that aims to make Discord a tiny bit more accessible for vision impaired users.

from os import environ
from dotenv import load_dotenv
import discord
from discord import option

load_dotenv()

if "TOKEN" not in environ:
    raise RuntimeError("TOKEN environment variable not set, exiting.")

__token__ = environ.get("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
bot = discord.Bot(intents=intents)

image_types = ["image/png", "image/jpeg", "image/aviv", "image/webp", "image/svg+xml"]

async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    """Gets executed when a message is sent in the server."""
    # Don't react to self or other bots to avoid a) recursion b) talking to a wall
    if message.author == bot.user or message.author.bot:
        return

    for attachment in message.attachments:
        if attachment.content_type in image_types:
            # Check if the image has a description.
            if not attachment.description:
                # React with an X to show an error
                message.add_reaction("❌")
                # The processing for the source message is complete

    # look for command prefix
    if message.content.startswith("!alt"):
        # get command content
        if message.reference is None:
            message.add_reaction("↩")
            message.add_reaction("❌")
        else:
            source_message = await message.channel.fetch_message(message.reference.message_id)
            alts = message.content.split("|")[4:]
            if (source_message.attachments is None or len(alts) != len(source_message.attachments)):
                message.add_reaction("#️⃣")
                message.add_reaction("❌")
            else:
                pattachments = source_message.attachments
                fixedFiles = []
                idx = 0
                for i in pattachments:
                    pattachments[i].description = alts[idx]
                    idx += 1
                    fixedFiles.append(pattachments[i])
                if source_message.content and source_message.content != "":
                    if idx > 1:
                        plural = "s"
                    else:
                        plural = ""
                    text = "_Re-Uploaded {}'s image{} with alt text by {}._\nOriginal message:\n\n{}".format(source_message.author.tag,plural,message.author.tag,source_message.content)
                    await message.channel.send(text, files=fixedFiles)
                else:
                    if idx > 1:
                        plural = "s"
                    else:
                        plural = ""
                    text = "_Re-Uploaded {}'s image{} with alt text by {}._".format(source_message.author.tag,plural,message.author.tag)
                    await message.channel.send(text, files=fixedFiles)
                message.delete()
                source_message.delete()

# Create a slash command for posting images with alt text on mobile
@bot.command(name="alt-text",description="Sends an image with alt text added.") # this decorator makes a slash command
@option(
    "Image1",
    discord.Attachment,
    description="An image to attach to the message",
    required=True,
)
@option(
    "Image2",
    discord.Attachment,
    description="An image to attach to the message",
    required=False,  # The default value will be None if the user doesn't provide a file.
)
@option(
    "Image3",
    discord.Attachment,
    description="An image to attach to the message",
    required=False,  # The default value will be None if the user doesn't provide a file.
)
@option(
    "Image4",
    discord.Attachment,
    description="An image to attach to the message",
    required=False,  # The default value will be None if the user doesn't provide a file.
)
@option(
    "Image5",
    discord.Attachment,
    description="An image to attach to the message",
    required=False,  # The default value will be None if the user doesn't provide a file.
)
@option("AltText1", description="Enter your alt text for Image 1", required=True)
@option("AltText2", description="Enter your alt text for Image 2", required=False)
@option("AltText3", description="Enter your alt text for Image 3", required=False)
@option("AltText4", description="Enter your alt text for Image 4", required=False)
@option("AltText5", description="Enter your alt text for Image 5", required=False)
@option("MessageText", description="Enter your message text", required=False)
async def altText(
    ctx: discord.ApplicationContext,
    Image1: discord.Attachment,
    Image2: discord.Attachment,
    Image3: discord.Attachment,
    Image4: discord.Attachment,
    Image5: discord.Attachment,
    AltText1: str,
    AltText2: str,
    AltText3: str,
    AltText4: str,
    AltText5: str,
    MessageText: str,
): # a slash command will be created with the name "alt-text" and the description "Sends an image with alt text added."
    fixedFiles = []
    Image1.description = AltText1
    fixedFiles.append(Image1)
    if Image2 is not None:
        if AltText2 is None:
            await ctx.respond("Error: You must enter alt text for every image you upload.")
            return
        Image2.description = AltText2
        fixedFiles.append(Image2)
    if Image3 is not None:
        if AltText3 is None:
            await ctx.respond("Error: You must enter alt text for every image you upload.")
            return
        Image3.description = AltText3
        fixedFiles.append(Image3)
    if Image4 is not None:
        if AltText4 is None:
            await ctx.respond("Error: You must enter alt text for every image you upload.")
            return
        Image4.description = AltText4
        fixedFiles.append(Image4)
    if Image5 is not None:
        if AltText5 is None:
            await ctx.respond("Error: You must enter alt text for every image you upload.")
            return
        Image5.description = AltText5
        fixedFiles.append(Image5)
    if MessageText is not None:
        await ctx.respond(MessageText, files=fixedFiles)
    else:
        await ctx.respond(files=fixedFiles)

# Connect the bot to the discord api
bot.run(__token__)