from typing import Optional, List

import discord
from discord import app_commands
from discord.ext import commands

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


class MyBot(commands.Bot):
    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


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
intents.message_content = True  # required for dropdown

# client = MyClient(intents=intents)
bot = MyBot(command_prefix='/', description='blah', intents=intents)
client = bot


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    # do an initial toon render here and set the bots pfp to it
    # ( might be good to do a headshot/toptoons pic for it as well
    pfp_path = "img/test/image_test.png"

    fp = open(pfp_path, 'rb')
    pfp = fp.read()
    await bot.user.edit(avatar = pfp)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name="toontow"))


def generateQuestEmbed(avName="Toon", questID=None):
    quests = localizer.QuestDialogDict
    if not questID:
        questID, dialog = random.choice(list(quests.items()))
    else:
        dialog = quests[questID]

    dialog = dialog.get(localizer.QUEST).replace('\a', '\n').replace('_avName_', f'**{avName}**')

    em = discord.Embed(
        title = "ToonTask",
        description = dialog,
    )
    em.set_footer(text=f"Quest ID: {questID}\nTotal Quest Entries: {len(quests)}", icon_url  = "attachment://task.png")

    file = discord.File("img/task.png", filename = "task.png")
    em.set_thumbnail(url = "attachment://task.png")
    return (em, file)


def generateNpcInfo(npcID):
    # set NpcInfo attrs here by looking up npcID stuff
    info = {
        "Building": "Gay Gaming Goober Group",
        "Location": "Punchline Place, Toontown Central",
        "Type": "Shopkeeper",
        "Random DNA": "False"
    }
    return info

def generateNPCRender(renderArgs):
    # generate toonsnapshot, pass args if needed?
    # replace this with toonsnapshot output
    file = discord.File("img/test/image_test.png", filename = "image_test.png")

    # get npc info
    npcID = renderArgs.get("NPC_ID")
    npcInfo = generateNpcInfo(npcID)

    em = discord.Embed(
        title = "NPC Toon",
        description = f"Rollo The Amazing",
    )
    em.set_image(url = "attachment://image_test.png")

    for name, value in npcInfo.items():
        em.add_field(name=name, value = value)

    em.set_footer(text=f"NPC ID: {npcID} (420 NPCs total)")
    return em, file


# Defines a custom Select containing colour options
# that the user can choose. The callback function
# of this class is called when the user changes their choice
class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Red', description='Your favourite colour is red', emoji='🟥'),
            discord.SelectOption(label='Green', description='Your favourite colour is green', emoji='🟩'),
            discord.SelectOption(label='Blue', description='Your favourite colour is blue', emoji='🟦'),
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Choose your favourite colour...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.response.send_message(f'Your favourite colour is {self.values[0]}')


# Define a simple View that gives us a confirmation menu
class ToggleRenderAttributesView(discord.ui.View):
    def __init__(self, embed):
        super().__init__()
        self.value = None
        self.embed = embed

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Toggle Nametag', style=discord.ButtonStyle.secondary)
    async def toggle_nametag(self, interaction: discord.Interaction, button: discord.ui.Button):
        file = discord.File("img/test/image_test_full.png", filename = "image_test_full.png")
        self.embed.set_image(url = "attachment://image_test_full.png")
        await interaction.response.edit_message(attachments = [file], embed = self.embed, view = self)
        # await interaction.response.send_message('Confirming', ephemeral=True)
        self.value = True
        # self.stop()

    @discord.ui.button(label='Randomize', style=discord.ButtonStyle.primary)
    async def new_render(self, interaction: discord.Interaction, button: discord.ui.Button):
        # re-render whatever we just rendered but ensure random dna, or random npc id, or random whatever is set
        await interaction.response.send_message(f'placeholder entry', ephemeral=True)


# Define a simple View that gives us a confirmation menu
class GenerateQuestView(discord.ui.View):
    def __init__(self, icon):
        super().__init__()
        self.icon = icon

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Random ToonTask', style=discord.ButtonStyle.primary)
    async def regenerate_quest(self, interaction: discord.Interaction, button: discord.ui.Button):
        em, file = generateQuestEmbed(interaction.user.display_name)
        await interaction.response.edit_message(embed = em, view = self)


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())


@client.command()
async def color(ctx):
    """Sends a message with our dropdown containing colours"""

    # Create the view containing our dropdown
    view = DropdownView()

    # Sending a message containing our view
    await ctx.send('Pick your favourite colour:', view=view)

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
async def quest(interaction: discord.Interaction, quest_id: Optional[int] = None):
    # QuestDialogDict may only be mainline tasks though.? if QuestDict focuses on JFF this will add on to the count

    em, file = generateQuestEmbed(interaction.user.display_name, questID=quest_id)
    # todo: integrate Quests.py to fix _where_ and others
    # todo: replace QuestDialogDict with Quests.QuestDict
    view = GenerateQuestView(file)

    await interaction.response.send_message(embed=em, view=view, file=file)
    await view.wait()

@client.tree.command()
async def holiday(interaction: discord.Interaction):
    holidays = localizer.HolidayNamesInCalendar
    id, holiday = random.choice(list(holidays.items()))
    em = discord.Embed(
        title = holiday[0],
        description = holiday[1]
    )
    em.set_footer(text = f"Holiday ID: {id}\nTotal Holiday Entries: {len(holidays)}")
    await interaction.response.send_message(embed=em)


# @client.tree.command()
# async def stats(interaction: discord.Interaction):
#     # collect cool toontown stats like total unique name combinations
#     holidays = localizer.HolidayNamesInCalendar
#     id, holiday = random.choice(list(holidays.items()))
#     em = discord.Embed(
#         title = holiday[0],
#         description = holiday[1]
#     )
#     em.set_footer(text = f"Holiday ID: {id}\nTotal Holiday Entries: {len(holidays)}")
#     await interaction.response.send_message(embed=em)


@client.tree.command()
async def building(interaction: discord.Interaction, count: Optional[bool] = False):
    bldgs = localizer.zone2TitleDict
    bldgName = ""
    if count:
        await interaction.response.send_message(f"Total Building Entries = {len(bldgs)}")
    else:
        # Since this command spits out building names, we don't want to it to print *nothing*
        while not bldgName:
            _, title = random.choice(list(bldgs.items()))
            bldgName = title[0]
        await interaction.response.send_message(bldgName)

@client.tree.command()
async def knockknock(interaction: discord.Interaction, general_jokes: Optional[bool] = True, contest_jokes: Optional[bool] = True):
    jokeChoices = []
    if general_jokes:
        jokeChoices += localizer.KnockKnockJokes
    if contest_jokes:
        # this is formatted much differently than the general jokes
        for jokeid in localizer.KnockKnockContestJokes.keys():
            if isinstance(localizer.KnockKnockContestJokes[jokeid], dict):
                for i in localizer.KnockKnockContestJokes[jokeid].keys():
                    jokeChoices += [localizer.KnockKnockContestJokes[jokeid][i]]
            else:
                jokeChoices += [localizer.KnockKnockContestJokes[jokeid]]

    if not jokeChoices:
        await interaction.response.send_message(f"Hey! You need at least one option to be True!", ephemeral=True)
        return

    jokeIndex = random.randrange(len(jokeChoices))
    first, second = jokeChoices[jokeIndex]

    em = discord.Embed(
        title = "Knock Knock Joke!",
        description = f"**Knock Knock**\n*Who's there?*\n**{first}**\n*{first} who?*\n**{second}**"
    )
    em.set_footer(text=f"Selected Joke #{jokeIndex} (out of {len(jokeChoices)})")

    await interaction.response.send_message(embed=em)

@client.tree.command()
async def emtest(interaction: discord.Interaction):


    # file2 = discord.File("img/test/image_toon_full.png", filename = "image_toon_full.png")

    # embed = discord.Embed()
    # await channel.send(file = file, embed = embed)
    em, file = generateNPCRender(RenderArgs)

    # in future, pass file since it'll be re=rendered
    # NB: make it easier just re-render and use that output??? but then cache.. fuck
    # maybe have an option to pass a custom file name to toonrender
    view = ToggleRenderAttributesView(embed=em)

    await interaction.response.send_message(files=[file], embed=em, view=view)
    await view.wait()
    if view.value is None:
        print('Timed out...')
    elif view.value:
        # this is where you would re-call the toon render operation?
        # actually this might be called after the view :b so no
        print("confirm")
    else:
        print('Cancelled...')

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



# extracted from localizer
# what if we did a lambda function and picked out 25 random npcs from the list
# lambda function should guarantee randomness each time the command is ran as a compensation to the 25 limit
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


def pickRandomNPCNames():
    npcRandomChoices = []
    for i in range(15):
        k, v = random.choice(list(NPCToonNames.items()))
        npcRandomChoices.append(
            app_commands.Choice(name = v, value = str(f"npc-{k}"))
        )
    return npcRandomChoices


async def npc_autocomplete(interaction: discord.Interaction, current:str) -> List[app_commands.Choice[str]]:
    options = []
    for i in range(15):
        k, v = random.choice(list(NPCToonNames.items()))
        # print([k, v])
        options.append([k, v])
    print(options)
    # for k, v in options:
    #     print(v)

    return [
        app_commands.Choice(name = entry[1], value = f"npc-{entry[0]}")
        for entry in options
    ]


async def fruit_autocomplete(
        interaction: discord.Interaction,
        current: str,
) -> List[app_commands.Choice[str]]:

    options = []
    for i in range(15):
        k, v = random.choice(list(NPCToonNames.items()))
        # print([k, v])
        options.append([k, v])
    # print(options)
    # for k, v in options:
    #     print(v)

    return [
        app_commands.Choice(name = entry[1], value = f"npc-{entry[0]}")
        for entry in options

    ]

    fruits = ['Banana', 'Pineapple', 'Apple', 'Watermelon', 'Melon', 'Cherry']
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ]

@client.tree.command()
@app_commands.autocomplete(fruit=fruit_autocomplete)
async def fruits(interaction: discord.Interaction, fruit: str):
    await interaction.response.send_message(f'Your favourite fruit seems to be {fruit}')


@client.tree.command()
@app_commands.describe(
    random_dna='Render a Random Toon',
    npc = "Name of NPC to render",
    toon_name = "Name of toon",
    nametag = "Display nametag"
)
@app_commands.autocomplete(
    npc = npc_autocomplete
)
#
# @app_commands.choices(npc=pickRandomNPCNames())

# npc: app_commands.Choice[str] = None,
async def toon(interaction: discord.Interaction,
               random_dna: Optional[bool] = True, npc: Optional[str] = None,
               toon_name: Optional[str] = None, nametag: Optional[bool] = True,
               frame_type: Optional[FrameType] = FrameType.Bodyshot,
               eye_type: Optional[EyeType] = EyeType.NormalOpen,
               chatbubble_type: Optional[ChatBubbleType] = ChatBubbleType.Normal,
               ):
    """Says when a member joined."""
    # If no member is explicitly provided then we use the command user here
    toonName = toon_name or 'Toon'
    # if not name, choose random name instead
    # if not nametag, then send command without nametag request
    # if npc = None do random npc
    # also for npc lookup npc by name2id

    RenderArgs[ChatBubbleType] = chatbubble_type
    RenderArgs[EyeType] = eye_type
    RenderArgs[FrameType] = frame_type


    # https://docs.python.org/3/library/enum.html
    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'rdna = {random_dna}, npc = {npc}, nametag = {nametag}. name= {toonName}'
                                            f'\n{repr(frame_type)}\n{repr(eye_type)}\n{repr(chatbubble_type)}')


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

