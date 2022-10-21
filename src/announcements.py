# Announcements cog for ERIS
# Written by Nate (@iNatie)
# A project that allows either plaintext messages or embeds to be sent to a channel, using a webhook to obufuscate the sender.

from os import environ
from dotenv import load_dotenv
import discord

load_dotenv()

if "TOKEN" not in environ:
    raise RuntimeError("TOKEN environment variable not set, exiting.")

__token__ = environ.get("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
bot = discord.Bot(intents=intents)
embed = discord.Embed()
sendToChannel = None

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

class Author(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Name", placeholder="Author Name", custom_id="author_name"))
        self.add_item(discord.ui.InputText(label="URL", placeholder="URL", custom_id="url"))
        self.add_item(discord.ui.InputText(label="Icon URL", placeholder="Icon URL", custom_id="icon_url"))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            description=embed.Description,
            color=embed.Color, # Pycord provides a class with default colors you can choose from
            author=discord.Author(name=self.children[0].value, url=self.children[1].value, icon_url=self.children[2].value),
            footer=embed.Footer,
            image=embed.Image,
            thumbnail=embed.Thumbnail,
            title=embed.Title,
            url=embed.URL,
            fields=embed.Fields
        )
        await interaction.response.edit_message(content="**PREVIEW**", embed=embed, view=embedButtons())

class Description(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Description", placeholder="Description", custom_id="description", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            description=self.children[0].value,
            color=embed.Color, # Pycord provides a class with default colors you can choose from
            author=embed.Author,
            footer=embed.Footer,
            image=embed.Image,
            thumbnail=embed.Thumbnail,
            title=embed.Title,
            url=embed.URL,
            fields=embed.Fields
        )
        await interaction.response.edit_message(content="**PREVIEW**", embed=embed, view=embedButtons())

class Footer(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Footer", placeholder="Footer", custom_id="footer"))
        self.add_item(discord.ui.InputText(label="Icon URL", placeholder="Icon URL", custom_id="footer_icon_url"))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            description=embed.Description,
            color=embed.Color, # Pycord provides a class with default colors you can choose from
            author=embed.Author,
            footer=discord.Footer(text=self.children[0].value, icon_url=self.children[1].value),
            image=embed.Image,
            thumbnail=embed.Thumbnail,
            title=embed.Title,
            url=embed.URL,
            fields=embed.Fields
        )
        await interaction.response.edit_message(content="**PREVIEW**", embed=embed, view=embedButtons())

class Image(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Image URL", placeholder="Image URL", custom_id="image_url"))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            description=embed.Description,
            color=embed.Color, # Pycord provides a class with default colors you can choose from
            author=embed.Author,
            footer=embed.Footer,
            image=discord.Image(url=self.children[0].value),
            thumbnail=embed.Thumbnail,
            title=embed.Title,
            url=embed.URL,
            fields=embed.Fields
        )
        await interaction.response.edit_message(content="**PREVIEW**", embed=embed, view=embedButtons())

class Thumbnail(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Thumbnail URL", placeholder="Thumbnail URL", custom_id="thumbnail_url"))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            description=embed.Description,
            color=embed.Color, # Pycord provides a class with default colors you can choose from
            author=embed.Author,
            footer=embed.Footer,
            image=embed.Image,
            thumbnail=discord.Thumbnail(url=self.children[0].value),
            title=embed.Title,
            url=embed.URL,
            fields=embed.Fields
        )
        await interaction.response.edit_message(content="**PREVIEW**", embed=embed, view=embedButtons())

class Title(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Title", placeholder="Title", custom_id="title"))
        self.add_item(discord.ui.InputText(label="URL", placeholder="URL", custom_id="title_url"))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            description=embed.Description,
            color=embed.Color, # Pycord provides a class with default colors you can choose from
            author=embed.Author,
            footer=embed.Footer,
            image=embed.Image,
            thumbnail=embed.Thumbnail,
            title=self.children[0].value,
            url=self.children[1].value,
            fields=embed.Fields
        )
        await interaction.response.edit_message(content="**PREVIEW**", embed=embed, view=embedButtons())

class FieldInline(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Should this field be inline?", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Yes",
                value="True",
                description="The field should be inline."
            ),
            discord.SelectOption(
                label="No",
                value="False",
                description="The field should not be inline."
            )
        ]
    )
    async def callback(self, interaction: discord.Interaction):
        global fieldInline
        fieldInline = self.values[0]

class FieldData(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Name", placeholder="Name", custom_id="field_name"))
        self.add_item(discord.ui.InputText(label="Value", placeholder="Value", custom_id="field_value"))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(FieldInline(title="FieldInline"))
        if fieldInline == "True":
            fInline = True
        else:
            fInline = False
        embed = discord.Embed(
            description=embed.Description,
            color=embed.Color, # Pycord provides a class with default colors you can choose from
            author=embed.Author,
            footer=embed.Footer,
            image=embed.Image,
            thumbnail=embed.Thumbnail,
            title=embed.Title,
            url=embed.URL,
            fields=embed.Fields + [discord.Field(name=self.children[0].value, value=self.children[1].value, inline=fInline)]
        )

class Color(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a Color", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Blurple",
                value="blurple",
                description="The default Discord color"
            ),
            discord.SelectOption(
                label="Blue",
                value="blue"
                description="It's blue"
            ),
            discord.SelectOption(
                label="Brand Green",
                value="brand_green"
                description="The color of the Discord green"
            )
            discord.SelectOption(
                label="Brand Red",
                value="brand_red"
                description="The color of the Discord red"
            )
            discord.SelectOption(
                label="Dark Blue",
                value="dark_blue"
                description="It's dark blue"
            )
            discord.SelectOption(
                label="Dark Gold",
                value="dark_gold"
                description="It's dark gold"
            )
            discord.SelectOption(
                label="Dark Gray",
                value="dark_gray"
                description="It's dark gray"
            )
            discord.SelectOption(
                label="Dark Green",
                value="dark_green"
                description="It's dark green"
            )
            discord.SelectOption(
                label="Dark Grey",
                value="dark_grey"
                description="It's dark grey"
            )
            discord.SelectOption(
                label="Dark Magenta",
                value="dark_magenta"
                description="It's dark magenta"
            )
            discord.SelectOption(
                label="Dark Orange",
                value="dark_orange"
                description="It's dark orange"
            )
            discord.SelectOption(
                label="Dark Purple",
                value="dark_purple"
                description="It's dark purple"
            )
            discord.SelectOption(
                label="Dark Red",
                value="dark_red"
                description="It's dark red"
            )
            discord.SelectOption(
                label="Dark Teal",
                value="dark_teal"
                description="It's dark teal"
            )
            discord.SelectOption(
                label="Dark Theme",
                value="dark_theme"
                description="The color of the Discord dark theme"
            )
            discord.SelectOption(
                label="Darker Gray",
                value="darker_gray"
                description="It's darker gray"
            )
            discord.SelectOption(
                label="Darker Grey",
                value="darker_grey"
                description="It's darker grey"
            )
            discord.SelectOption(
                label="Default",
                value="default"
                description="The default color"
            )
            discord.SelectOption(
                label="Fuchsia",
                value="fuchsia"
                description="It's fuchsia"
            )
            discord.SelectOption(
                label="Gold",
                value="gold"
                description="It's gold"
            )
            discord.SelectOption(
                label="Greyple",
                value="greyple"
                description="The default Discord color, but grey"
            )
            discord.SelectOption(
                label="Light Gray",
                value="light_gray"
                description="It's light gray"
            )
            discord.SelectOption(
                label="Light Grey",
                value="light_grey"
                description="It's light grey"
            )
            discord.SelectOption(
                label="Lighter Gray",
                value="lighter_gray"
                description="It's lighter gray"
            )
            discord.SelectOption(
                label="Lighter Grey",
                value="lighter_grey"
                description="It's lighter grey"
            )
            discord.SelectOption(
                label="Magenta",
                value="magenta"
                description="It's magenta"
            )
            discord.SelectOption(
                label="OG Blurple",
                value="og_blurple"
                description="The original Discord color"
            )
            discord.SelectOption(
                label="Orange",
                value="orange"
                description="It's orange"
            )
            discord.SelectOption(
                label="Purple",
                value="purple"
                description="It's purple"
            )
            discord.SelectOption(
                label="Random",
                value="random"
                description="A random color"
            )
            discord.SelectOption(
                label="Red",
                value="red"
                description="It's red"
            )
            discord.SelectOption(
                label="Teal",
                value="teal"
                description="It's teal"
            )
            discord.SelectOption(
                label="Yellow",
                value="yellow"
                description="It's yellow"
            )
        ]
    )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            description=embed.Description,
            coloring = self.children[0].value+"()"
            color=discord.Color.coloring, # Pycord provides a class with default colors you can choose from
            author=embed.Author,
            footer=embed.Footer,
            image=embed.Image,
            thumbnail=embed.Thumbnail,
            title=embed.Title,
            url=embed.URL,
            fields=embed.Fields
        )
        await interaction.response.edit_message(content="**PREVIEW**", embed=embed, view=embedButtons())

class embedButtons(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Author", row=0, style=discord.ButtonStyle.primary) # Create a button with the label "Author" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(Author(title="Author")) # Open a text modal when the button is clicked
    @discord.ui.button(label="Color", row=0, style=discord.ButtonStyle.primary) # Create a button with the label "Color" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(Color(title="Color")) # Open a text modal when the button is clicked
    @discord.ui.button(label="Description", row=0, style=discord.ButtonStyle.primary) # Create a button with the label "Description" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(Description(title="Description")) # Open a text modal when the button is clicked
    @discord.ui.button(label="Footer", row=0, style=discord.ButtonStyle.primary) # Create a button with the label "Footer" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(Footer(title="Footer"))
    @discord.ui.button(label="Image", row=1, style=discord.ButtonStyle.primary) # Create a button with the label "Image" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(Image(title="Image"))
    @discord.ui.button(label="Thumbnail", row=2, style=discord.ButtonStyle.primary) # Create a button with the label "Thumbnail" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(Thumbnail(title="Thumbnail"))
    @discord.ui.button(label="Title (with URL)", row=2, style=discord.ButtonStyle.primary) # Create a button with the label "Title (with URL)" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(Title(title="Title"))
    @discord.ui.button(label="Add Field", row=3, style=discord.ButtonStyle.primary) # Create a button with the label "Add Field" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(FieldData(title="Field Data"))
    @discord.ui.button(label="Send", row=4, style=discord.ButtonStyle.green) # Create a button with the label "Send" with color Green
    async def button_callback(self, button, interaction):
        channel = bot.get_channel(sendToChannel)
        if channel:
            await channel.send(embed=embed)
            await interaction.response.send_message("Embed sent!", ephemeral=True)

# create Slash Command group with bot.create_group
announce = bot.create_group("announce", "Announce a message to a channel.")
@announce.command()
async def text(ctx, channel: discord.TextChannel, message: str):
    try:
        await channel.send(message)
        await ctx.respond(f"Message sent to , {channel}!")
    except:
        await ctx.respond("Error: I don't have permission to send messages to that channel.")

@announce.command()
async def embed(ctx, channel: discord.TextChannel):
    sendToChannel = channel
    embed = discord.Embed(
        description = "Hello! This is the default description.\nYou can customize this embed by using the buttons below.\nTo remove this message, change the description.\n\nSome formatting tips:\n*Italic*: Italic\n**Bold**: Bold\n~~Strikethrough~~: Strikethrough\n___Underline___: Underline\n[Website](https://discord.com/): Website\n`Code block`: Code block",
        color=discord.Colour.orange(), # Pycord provides a class with default colors you can choose from
    )
    await ctx.respond("**PREVIEW**", embed=embed, view=embedButtons())

bot.run("your token here")