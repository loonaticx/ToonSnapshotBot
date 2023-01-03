from typing import Optional

import discord
from discord import app_commands

from app_commands import localizer
import random
from config import config
from RenderEnums import *

MY_GUILD = discord.Object(id=config.BOT_GUILD)  # replace with your guild id

RenderArgs = {
    # /render
    RenderType: RenderType.Toon,
    "WANT_NAMETAG": True,
    ChatBubbleType: ChatBubbleType.Normal,
    "CUSTOM_PHRASE": None,  # alt to speedchat phrase; not none = user gave input
    FrameType: FrameType.Bodyshot,

    # /render: context-specific
    "NAME": None,  # generate random if None
    "DNA_RANDOM": True,
    "SPEEDCHAT_PHRASE": None,  # speedchat phrase id if not None
    "POSE_PRESET": None,  # context specific, None -> random
    "DNA_STRING": None,  # generate random dna if None, might be a literal dna (list; not netstring)

    # /toon and /npc
    EyeType: EyeType.NormalOpen,
    MuzzleType: MuzzleType.Neutral,

    # /npc
    "NPC_ID": None,  # none -> random


}

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')


@client.tree.command()
@app_commands.describe(
    first_value='The first value you want to add something to',
    second_value='The value you want to add to the first value',
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int):
    """Adds two numbers together."""
    await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')


# The rename decorator allows us to change the display of the parameter on Discord.
# In this example, even though we use `text_to_send` in the code, the client will use `text` instead.
# Note that other decorators will still refer to it as `text_to_send` in the code.
@client.tree.command()
async def quest(interaction: discord.Interaction, count: Optional[bool] = False):
    quests = localizer.QuestDialogDict
    """Sends the text into the current channel."""
    if count:
        # QuestDialogDict may only be mainline tasks though.? if QuestDict focuses on JFF this will add on to the count
        await interaction.response.send_message(f"Total Quest Entries = {len(quests)}")
    else:
        _, dialog = random.choice(list(quests.items()))
        dialog = dialog.get(localizer.QUEST).replace('\a', '\n').replace('_avName_', f'**{interaction.user.display_name}**')
        # todo: integrate Quests.py to fix _where_ and others
        # todo: replace QuestDialogDict with Quests.QuestDict
        await interaction.response.send_message(dialog)

@client.tree.command()
async def holiday(interaction: discord.Interaction, count: Optional[bool] = False):
    holidays = localizer.HolidayNamesInCalendar
    """Sends the text into the current channel."""
    if count:
        await interaction.response.send_message(f"Total Holiday Entries = {len(holiday)}")
    else:
        title, dialog = random.choice(list(holidays.items()))
        await interaction.response.send_message(f"**{title}**\n{dialog}")


@client.tree.command()
async def building(interaction: discord.Interaction, count: Optional[bool] = False):
    bldgs = localizer.zone2TitleDict
    bldgName = ""
    """Sends the text into the current channel."""
    if count:
        await interaction.response.send_message(f"Total Building Entries = {len(bldgs)}")
    else:
        while not bldgName:
            _, title = random.choice(list(bldgs.items()))
            bldgName = title[0]
        await interaction.response.send_message(bldgName)

@client.tree.command()
async def knockknock(interaction: discord.Interaction, general_jokes: Optional[bool] = True, contest_jokes: Optional[bool] = True, count: Optional[bool] = False):
    jokeChoices = []
    if general_jokes:
        jokeChoices += localizer.KnockKnockJokes
    if contest_jokes:
        jokeChoices += localizer.KnockKnockContestJokes

    if not jokeChoices:
        await interaction.response.send_message(f"Hey! You need at least one option to be True!", ephemeral=True)
        return

    """Sends the text into the current channel."""
    if count:
        # QuestDialogDict may only be mainline tasks though.? if QuestDict focuses on JFF this will add on to the count
        await interaction.response.send_message(f"Total Joke Entries = {len(jokeChoices)}")
    else:
        first, second = random.choice(jokeChoices)
        await interaction.response.send_message(f"**Knock Knock**\n*Who's there?*\n**{first}**\n*{first} who?*\n**{second}**")

@client.tree.command()
async def toontip(interaction: discord.Interaction,
                  general_tip: Optional[bool] = True, street_tip: Optional[bool] = True,
                  minigame_tip: Optional[bool] = True, coghq_tip: Optional[bool] = True,
                  estate_tip: Optional[bool] = True, karting_tip: Optional[bool] = True,
                  golf_tip: Optional[bool] = True,
                  count: Optional[bool] = False):
    tips = localizer.TipDict
    # del tips[localizer.TIP_NONE]
    tipChoices = ()
    if general_tip:
        tipChoices += tips[localizer.TIP_GENERAL]
    if street_tip:
        tipChoices += tips[localizer.TIP_STREET]
    if minigame_tip:
        tipChoices += tips[localizer.TIP_MINIGAME]
    if coghq_tip:
        tipChoices += tips[localizer.TIP_COGHQ]
    if estate_tip:
        tipChoices += tips[localizer.TIP_ESTATE]
    if karting_tip:
        tipChoices += tips[localizer.TIP_KARTING]
    if golf_tip:
        tipChoices += tips[localizer.TIP_GOLF]

    if not tipChoices:
        await interaction.response.send_message(f"Hey! You need at least one option to be True!", ephemeral=True)
        return

    """Sends the text into the current channel."""
    if count:
        # QuestDialogDict may only be mainline tasks though.? if QuestDict focuses on JFF this will add on to the count
        await interaction.response.send_message(f"Total Toon Tip Entries = {len(tipChoices)}")
    else:
        tip = random.choice(tipChoices)
        await interaction.response.send_message(tip)


# To make an argument optional, you can either give it a supported default argument
# or you can mark it as Optional from the typing standard library. This example does both.

npcnamechoices = [
    'bob',
    'flippy',
    'geezer',
    'man'
]


# extracted from localizer
npcnametest = {
    3127: "Ifalla Yufalla",
    3128: "Sticky George",
    3129: "Baker Bridget",
    3130: "Sandy",
    3131: "Lazy Lorenzo",
    3132: "Ashy",
    3133: "Dr. Friezeframe",
    3134: "Lounge Lassard",
    3135: "Soggy Nell",
    3136: "Happy Sue",
    3137: "Mr. Freeze",
    3138: "Chef Bumblesoup",
    3139: "Granny Icestockings",
    3140: "Fisherman Lucille",
}

from localizer import NPCToonNames

npcChoices = []

for k, v in npcnametest.items():
    # print(k)
    # print(v)
    # print("======")
    npcChoices.append(
        app_commands.Choice(name=v, value=str(f"npc-{k}"))
    )



@client.tree.command()
@app_commands.describe(
    random_dna='Render a Random Toon',
    npc = "Name of NPC to render",
    toon_name = "Name of toon",
    nametag = "Display nametag"
)
# @app_commands.autocomplete(
#     npc = npcnamechoices
# )

@app_commands.choices(npc=npcChoices)
async def toon(interaction: discord.Interaction,
               random_dna: Optional[bool] = True, npc: app_commands.Choice[str] = None,
               toon_name: Optional[str] = None, nametag: Optional[bool] = True):
    """Says when a member joined."""
    # If no member is explicitly provided then we use the command user here
    toonName = toon_name or 'Toon'
    # if not name, choose random name instead
    # if not nametag, then send command without nametag request
    # if npc = None do random npc
    # also for npc lookup npc by name2id

    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'rdna = {random_dna}, npc = {npc}, nametag = {nametag}. name= {toonName}')


# A Context Menu command is an app command that can be run on a member or on a message by
# accessing a menu within the client, usually via right clicking.
# It always takes an interaction as its first parameter and a Member or Message as its second parameter.

# This context menu command only works on members
@client.tree.context_menu(name='Show Join Date')
async def show_join_date(interaction: discord.Interaction, member: discord.Member):
    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')


# This context menu command only works on messages
@client.tree.context_menu(name='Report to Moderators')
async def report_message(interaction: discord.Interaction, message: discord.Message):
    # We're sending this response message with ephemeral=True, so only the command executor can see it
    await interaction.response.send_message(
        f'Thanks for reporting this message by {message.author.mention} to our moderators.', ephemeral=True
    )

    # Handle report by sending it into a log channel
    log_channel = interaction.guild.get_channel(0)  # replace with your channel id

    embed = discord.Embed(title='Reported Message')
    if message.content:
        embed.description = message.content

    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    embed.timestamp = message.created_at

    url_view = discord.ui.View()
    url_view.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))

    await log_channel.send(embed=embed, view=url_view)


client.run(config.BOT_TOKEN)

