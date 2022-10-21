# Related-Servers_Publisher cog for ERIS
# Written by Nate (@iNatie)
# A project that syncs a google sheet to a channel using embeds.
# Google Sheets API is used to get the data from the sheet. https://developers.google.com/sheets/api/quickstart/python

from os import environ
from dotenv import load_dotenv
import discord
import pandas as pd

load_dotenv()

if "TOKEN" not in environ:
    raise RuntimeError("TOKEN environment variable not set, exiting.")

__token__ = environ.get("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
bot = discord.Bot(intents=intents)
delay = 5 # seconds
channel = bot.get_channel(1017852432237199370) #Channel ID for Related-Servers
url="https://docs.google.com/spreadsheets/d/e/2PACX-1vSCO7f2uB-jKpEgsR97rYEqyAl9J-XAWKGEc7BS8ySJhZzPAJq24ssj0jH6OM_JyRYJjMmZn2O6Paf6/pub?gid=1470603482&single=true&output=csv"

#Set default Embed variable values/ values for Under Construction Message
title = '<:RLConstruction:1020583071612936222> Related-Servers is being refreshed'
rgb1 = 247 #RIT Orange
rgb2 = 105 #RIT Orange
rgb3 = 2 #RIT Orange
description = 'The Related-Servers channel is being refreshed; please be patient as we add new servers and update old ones.'
url = ''
FieldName = ''
FieldValue = ''
image = 'https://media.discordapp.net/attachments/1019604664532095038/1019605448577536050/unknown.png'
thumbnail = 'https://cdn.discordapp.com/icons/991686482618232873/a_08aedbaaf6fd0ddc7969f57bf5741b6f.gif'

def newEmbed():
    embed = discord.Embed(emTitle=title, emDescription=description)
    if url != "":
        embed.url = url
    if Color != "":
        embed.color = discord.color.from_rgb(rgb1, rgb2, rgb3)))
    if image != "":
        embed.set_image(url=image)
    if thumbnail != "":
        embed.set_thumbnail(url=thumbnail)
    if fieldName != "" and fieldValue != "":
        embed.add_field(name=fieldName, value=fieldValue, inline=True)
    await asyncio.sleep(delay)
    return embed

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
# Create a slash command
@bot.command(name="rl",description="Updates the Related-Servers embeds from a csv file") # this decorator makes a slash command
async def rl(ctx):
    await ctx.respond("Updating Related-Servers embeds, please be patient...")
    await ctx.channel.purge(bulk=True, reason='Refreshing Related-Servers' check=lambda m: m.author == bot.user)

    await channel.send(embed=newEmbed())

    data = pd.read_csv(url)

    dict = {'Timestamp': 'Timestamp',
            'Please create a permanent discord server link, or insert your vanity URL': 'Link',
            'What category fits you best?': 'Category',
            'Write a short description!': 'Description',
            'Provide an imgur link to an image we can use as an icon.': 'Icon',
            'If you are an RIT club/community, would you like access to our announcement channel to advertise events for your club?': 'Users',
            "What's your server's name?": 'Name',
            'DataPoint 1': 'DP1',
            'DP 2': 'DP2',
            'DP 3': 'DP3',
            'DP 4': 'DP4',}

    data = data.rename(columns=dict, inplace=True)

    if len(data.index) > 15:
        Repeat = (len(data.index)/15)*60 #Get the number of seconds to delay (Anything over 15 will trigger)
        Delay = Delay+(Round(Repeat,0)/len(data.index)) #Split the total delay time into even chunks per embed, then add on top of the default 5 second delay

    for i in range(len(data.index)):
        url = data['Link'][i]
        category = data['Category'][i]
        desc = data['Description'][i]
        thumb = data['Icon'][i]
        name = data['Name'][i]
        embed = newEmbed()
        datapoints = [data['DP1'][i], data['DP2'][i], data['DP3'][i], data['DP4'][i]]
        datapoints = [i for i in datapoints if i] # using list comprehension to perform removal

        elif category == "Clubs":
            title = '<:RLStar:1020388439511810220> '+name #Add Star emoji to name
            rgb1 = 0 #blue
            rgb2 = 133 #blue
            rgb3 = 255 #blue
            description = '<:bulletpoint:997516856975958138>**Category:** Clubs' #Set the Category 
            image = 'https://i.imgur.com/JC28QuU.png' #Set the divider bar color
        
        if category == "Colleges":
            title = '<:RLOffice:1020388437687279656> '+name #Add Office emoji to name
            rgb1 = 247 #RIT Orange
            rgb2 = 105 #RIT Orange
            rgb3 = 2 #RIT Orange
            description = '<:bulletpoint:997516856975958138>**Category:** College' #Set the Category
            image = 'https://i.imgur.com/5wRH6cH.png' #Set the divider bar color
        
        elif category == "Communities":
            title = '<:RLHeart:1020388428644356096> '+name #Add Heart emoji to name
            rgb1 = 208 #red
            rgb2 = 2 #red
            rgb3 = 27 #red
            description = '<:bulletpoint:997516856975958138>**Category:** Communities' #Set the Category 
            image = 'https://i.imgur.com/wOItiJK.png' #Set the divider bar color
        
        elif category == "Education":
            title = '<:RLMortar_Board:1020388435946651718> '+name #Add Mortar Board emoji to name
            rgb1 = 64 #Teal
            rgb2 = 224 #Teal
            rgb3 = 208 #Teal
            description = '<:bulletpoint:997516856975958138>**Category:** Education' #Set the Category 
            image = 'https://i.imgur.com/WF6fsPz.png' #Set the divider bar color
        
        elif category == "Gaming":
            title = '<:RLgame_controller:1020388425074999396> '+name #Add Game Controller emoji to name
            rgb1 = 248 #yellow
            rgb2 = 231 #yellow
            rgb3 = 28 #yellow
            description = '<:bulletpoint:997516856975958138>**Category:** Gaming' #Set the Category 
            image = 'https://i.imgur.com/Hv4lOyK.png' #Set the divider bar color

        elif category == "Housing":
            title = '<:RLHouse:1020388433467818075> '+name #Add House emoji to name
            rgb1 = 65 #green
            rgb2 = 117 #green
            rgb3 = 5 #green
            description = '<:bulletpoint:997516856975958138>**Category:** Housing' #Set the Category 
            image = 'https://i.imgur.com/BVxDvBK.png' #Set the divider bar color

        elif category == "Support/Advocacy":
            title = '<:RLHeart_Stars:1020388430661816342> '+name #Add Starry Heart emoji to name
            rgb1 = 144 #purple
            rgb2 = 19 #purple
            rgb3 = 254 #purple
            description = '<:bulletpoint:997516856975958138>**Category:** Support/Advocacy' #Set the Category 
            image = 'https://i.imgur.com/0DrLtqH.png' #Set the divider bar color

        else:
            title = '<:RLWave:1020388441978044567> '+name #Add Handwaving emoji to name
            rgb1 = 155 #gray
            rgb2 = 155 #gray
            rgb3 = 155 #gray
            description = '<:bulletpoint:997516856975958138>**Category:** '+category #Set the Category (Use custom element since it's "Other")
            image = 'https://i.imgur.com/vyOTfUN.png' #Set the divider bar color

        foreach datapoint in datapoints:
            description = description + '\n<:bulletpoint:997516856975958138>'+datapoint+ #Add each datapoint to the description

        FieldName = 'About:'
        FieldValue = desc
        thumbnail = thumb
        await channel.send(embed=newEmbed())
    
    #Set Embed variable values for How to Add Your Server Message
    title = '<a:tigerspin:1005552080884351076> Want to add a server to this channel?'
    rgb1 = 247 #RIT Orange
    rgb2 = 105 #RIT Orange
    rgb3 = 2 #RIT Orange
    description = 'If you have a server you'+"'"+'d like to add, fill out the linked Google Form (requires an RIT account, click the embed title "Want to add a server?" to access).'+"`n"+'Once you submit the form, we'+"'"+'ll add it with our next batch.'+"`n"+'Make a <#991686483763273810> ticket if you have any questions.'
    url = 'https://forms.gle/SM8rks1fgJ6WhJUt5'
    FieldName = ''
    FieldValue = ''
    image = ''
    thumbnail = ''
    await channel.send(embed=newEmbed()) #Send the How to Add Your Server Message

    #Set Embed variable values for How to Add Your Server Message
    title = '<a:tigerspin:1005552080884351076> How to join a server?'
    rgb1 = 247 #RIT Orange
    rgb2 = 105 #RIT Orange
    rgb3 = 2 #RIT Orange
    description = 'Click the titles, they are the URL links.'
    url = ''
    FieldName = ''
    FieldValue = ''
    image = 'https://i.imgur.com/x9yFMcz.jpg'
    thumbnail = ''
    await channel.send(embed=newEmbed()) #Send the How to Add Your Server Message

    await ctx.respond("Related-Servers has been updated successfully!")
