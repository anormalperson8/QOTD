# Packages
import nextcord
import os
from dotenv import load_dotenv
from nextcord.ext import commands
import datetime
import calendar
import asyncio

# Self .py files
import info_command
import server_info
import pageClass
import question

intents = nextcord.Intents.all()
client = commands.Bot(command_prefix='!q', intents=intents, help_command=None,
                      activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="out for questions"))

path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
load_dotenv(f"{path}/data/data.env")
token = os.getenv('TOKEN')
owner_id = int(os.getenv('ID'))
guilds_list = []
servers = server_info.get_servers()


@client.event
async def on_ready():
    await client.wait_until_ready()
    # client.loop.create_task(ask())
    global guilds_list
    for guild in client.guilds:
        guilds_list.append(int(guild.id))
    print('We have logged in as {0.user}'.format(client))
    test_server = server_info.get_servers()[0]
    channel_test = client.get_guild(test_server.serverID).get_channel(test_server.question_channel)
    await channel_test.send(f"Bot is on.")


# Response-testing command
@client.command()
async def boo(ctx):
    if ctx.author.bot:
        await ctx.send("You're not a user :P")
        return
    await ctx.send(f"Oi.")


@client.slash_command(guild_ids=guilds_list, description="Pong!")
async def ping(interaction: nextcord.Interaction):
    await interaction.response.defer(ephemeral=True)
    await interaction.edit_original_message(content="Pong!")


def timestamp():
    now = datetime.datetime.now()
    return f"Today is {now.date().day} {calendar.month_name[now.date().month]}, {now.date().year}\n" \
        f"The time (hh/mm/ss) now is {now.time().hour:02}:{now.time().minute:02}:{now.time().second:02}.\n" \
        f"Today is {calendar.day_name[now.weekday()]}."


@client.command()
async def time(ctx):
    if ctx.author.id != owner_id:
        return
    await ctx.send(f"Time check!\n{timestamp()}")


async def echo_content(ctx, arg, stat: bool):
    # Owner Privileges
    if ctx.author.id == owner_id:
        if ctx.message.reference is not None and ctx.message.reference.resolved is not None:
            await ctx.message.reference.resolved.reply(arg, mention_author=stat)
        else:
            await ctx.send(arg)
        return
    # Check Mod
    for role in ctx.message.author.roles:
        if role.id in server_info.search_for_server(servers, ctx.message.guild.id).moderator_roles:
            if ctx.message.reference is not None and ctx.message.reference.resolved is not None:
                await ctx.message.reference.resolved.reply(arg, mention_author=stat)
            else:
                await ctx.send(arg)
            return


@commands.guild_only()
@client.command()
async def echo(ctx, *, arg):
    await ctx.message.delete()
    await echo_content(ctx, arg, True)


@commands.guild_only()
@client.command()
async def echo2(ctx, *, arg):
    await ctx.message.delete()
    await echo_content(ctx, arg, False)


# Check whether the member is in the server, and whether users are allowed to use commands in the channel
def check_user(user_id, interaction):
    # Block users not in server
    if interaction.guild.get_member(user_id) is None:
        return 0
    # Only allow specific channels
    server = server_info.search_for_server(servers, interaction.guild_id)
    if interaction.channel_id not in server.allowedChannels:
        return 1
    return None


# Check whether a user is mod
def check_mod(interaction: nextcord.Interaction):
    for role in interaction.user.roles:
        if role.id in server_info.search_for_server(servers, interaction.guild_id).moderator_roles:
            return True
    return False


async def owner_reject(interaction: nextcord.Interaction):
    if interaction.user.id != owner_id:
        await interaction.edit_original_message(
            content="Did you not read the description? This is for the owner not you <:sunnyyBleh:1055108393372749824>")
        return True
    return False


@commands.guild_only()
@client.slash_command(guild_ids=guilds_list, description="My info!")
async def info(interaction: nextcord.Interaction):
    # server = server_info.search_for_server(servers, interaction.guild_id)
    title = "QOTD Eevee <:EeveeWave:1062326395935674489>"
    url = "https://github.com/anormalperson8/QOTD_Eevee"
    pages = [info_command.create_page(title, url, i + 1) for i in range(4)]
    image = "https://github.com/anormalperson8/QOTD_Eevee/blob/master/image/QOTD_Eevee.png?raw=true"
    for i in range(len(pages)):
        pages[i].set_thumbnail(image)
        pages[i].set_footer(text=f"Page {i + 1}/4")
    await interaction.response.send_message(content="", embed=pages[0],
                                            view=pageClass.InfoPages(pages=pages, ctx=interaction))


@commands.guild_only()
@client.slash_command(guild_ids=guilds_list, description="Add a reaction to a message. Must be used in the same "
                                                         "channel as the target message. Mods only.")
async def add_emote(interaction: nextcord.Interaction,
                    message_id: str = nextcord.SlashOption(required=True, description="The ID of the message."),
                    emote: str = nextcord.SlashOption(required=True, description="The emoji you want to add.")):
    await interaction.response.defer(ephemeral=True)
    if not check_mod(interaction):
        await interaction.edit_original_message(content="Mods only.")
        return
    try:
        if message_id.isnumeric():
            message = await interaction.channel.fetch_message(message_id)
        else:
            await interaction.edit_original_message(content="Not a valid id.")
            return
    except nextcord.NotFound or nextcord.HTTPException or nextcord.InvalidArgument:
        await interaction.edit_original_message(content="Message not found./Emote does not exist.")
        return
    await message.add_reaction(emote)
    await interaction.edit_original_message(content="Done.")


@commands.guild_only()
@client.slash_command(guild_ids=guilds_list, description="Secret Command. Owner only.")
async def secret(interaction: nextcord.Interaction,
                 number: int = nextcord.SlashOption(required=False, description="A number.", default=1)):
    await interaction.response.defer(ephemeral=True)
    if interaction.user.id != owner_id:
        await interaction.edit_original_message(
            embed=nextcord.Embed(colour=info_command.random_colour(), title="This is a secret🤫",
                                 url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                                 description="There is totally not a link at the title."))
        return
    global client
    content = "Guilds I am in: "
    for guild in client.guilds:
        content += f"\n{guild.name}: {guild.id}"
    if number:
        await interaction.edit_original_message(content=content,
                                                files=[nextcord.File(r"./data/server.json"),
                                                       nextcord.File(r"./data/filter.txt"),
                                                       nextcord.File(r"./data/questions.txt")])
        return
    await interaction.edit_original_message(content=content,
                                            files=[nextcord.File(r"./data/server.json"),
                                                   nextcord.File(r"./data/filter.txt"),
                                                   nextcord.File(r"./data/questions.txt"),
                                                   nextcord.File(r"./data/data.env")])


@commands.guild_only()
@client.slash_command(guild_ids=guilds_list, description="Edits a message Eevee sent. Mods only.")
async def edit(interaction: nextcord.Interaction,
               message_id: str = nextcord.SlashOption(required=True, description="The ID of the message."),
               content: str = nextcord.SlashOption(required=True, description="The new content of the message.")):
    await interaction.response.defer(ephemeral=True)
    if not check_mod(interaction):
        await interaction.edit_original_message(content="Mods only.")
        return
    try:
        if message_id.isnumeric():
            message = await interaction.channel.fetch_message(message_id)
        else:
            await interaction.edit_original_message(content="Not a valid id.")
            return
    except nextcord.NotFound or nextcord.HTTPException or nextcord.InvalidArgument:
        await interaction.edit_original_message(content="Message not found.")
        return
    if message.author.id == client.user.id:
        await message.edit(content=content)
        await interaction.edit_original_message(content="Done.")
    else:
        await interaction.edit_original_message(content="That message is not mine!")


@commands.guild_only()
@client.slash_command(guild_ids=guilds_list, description="Changes Eevee's activity. "
                                                         "Add url only when streaming. Owner only.")
async def activity(interaction: nextcord.Interaction,
                   activity_name: str = nextcord.SlashOption(required=True, description="The name of the application. "
                                                                                        "Put anything when deleting."),
                   verb: str = nextcord.SlashOption(
                       required=True,
                       choices={"Play": "Playing", "Stream": "Streaming",
                                "Listen": "Listening", "Watch": "Watching", "Delete": "None"},
                       description="The action."),
                   url: str = nextcord.SlashOption(
                       required=False,
                       description="The url. Add only when streaming.",
                       default=None)):
    await interaction.response.defer(ephemeral=True)
    if owner_reject(interaction):
        return
    verb_dict = {"Playing": nextcord.Game(name=activity_name),
                 "Streaming": nextcord.Streaming(name=activity_name, url=url),
                 "Listening": nextcord.Activity(type=nextcord.ActivityType.listening, name=activity_name),
                 "Watching": nextcord.Activity(type=nextcord.ActivityType.watching, name=activity_name),
                 "None": None}
    await client.change_presence(activity=verb_dict[verb])
    if verb == "None":
        await interaction.edit_original_message(content=f"Done. Activity is deleted.")
    elif verb == "Listening":
        await interaction.edit_original_message(content=f"Done. Activity is changed to \"{verb} to {activity_name}\".")
    else:
        await interaction.edit_original_message(content=f"Done. Activity is changed to \"{verb} {activity_name}\".")


@commands.guild_only()
@client.slash_command(guild_ids=guilds_list, description="Changes Eevee's status. "
                                                         "Add url only when streaming. Owner only.")
async def status(interaction: nextcord.Interaction,
                 stat: str = nextcord.SlashOption(
                     required=True,
                     choices={"Online": "Online", "Idle": "Idle",
                              "Do Not Disturb": "DND", "Offline": "Offline"},
                     description="The status.")):
    await interaction.response.defer(ephemeral=True)
    if owner_reject(interaction):
        return
    status_dict = {"Online": nextcord.Status.online, "Idle": nextcord.Status.idle,
                   "DND": nextcord.Status.dnd, "Offline": nextcord.Status.offline}
    await client.change_presence(status=status_dict[stat])
    await interaction.edit_original_message(content=f"Done.")


@commands.guild_only()
@client.slash_command(guild_ids=guilds_list, description="Changes server information. Owner only.")
async def modify(interaction: nextcord.Interaction,
                 server_id: str = nextcord.SlashOption(required=True, description="The server to edit."),
                 action: int = nextcord.SlashOption(required=True,
                                                    choices={"Add": 1,
                                                             "Remove": 0},
                                                    description="Add or remove an attribute."),
                 thing_to_modify: int = nextcord.SlashOption(required=True,
                                                             choices={"Questioning Channel": 1,
                                                                      "Moderator Role": 2,
                                                                      "Role to Ping": 3
                                                                      },
                                                             description="The attribute you want to edit."),
                 change: str = nextcord.SlashOption(required=False,
                                                    description="The ID you want to add/remove. "
                                                                "Write any number when removing ann/role",
                                                    default="")):
    await interaction.response.defer(ephemeral=True)
    if owner_reject(interaction):
        return
    # Changing data types
    action = bool(action)
    try:
        server_id = int(server_id)
    except ValueError:
        await interaction.edit_original_message(content="Invalid server ID.")
        return
    if change != "":
        try:
            change = int(change)
        except ValueError:
            await interaction.edit_original_message(content="Invalid channel/role ID.")
            return

    stat = False
    message = ""
    match thing_to_modify:
        case 1:
            if action and change == "":
                await interaction.edit_original_message(content=f"Problem: You forgot to include the ID.")
                return
            if change == "":
                change = 1
            stat, message = server_info.modify(server_id, action, question_channel=change)
        case 2:
            if change == "":
                await interaction.edit_original_message(content=f"Problem: You forgot to include the ID.")
                return
            stat, message = server_info.modify(server_id, action, moderator_role=change)
        case 3:
            if action and change == "":
                await interaction.edit_original_message(content=f"Problem: You forgot to include the ID.")
                return
            if change == "":
                change = 1
            stat, message = server_info.modify(server_id, action, role_to_ping=change)

    if stat:
        global servers
        servers = server_info.get_servers()
        await interaction.edit_original_message(content=f"Your modification is done!\n{message}")
        return
    await interaction.edit_original_message(content=f"Your modification was not completed.\n{message}")


@commands.guild_only()
@client.slash_command(guild_ids=guilds_list, description="Add a server to the server file. Owner only.")
async def add_server(interaction: nextcord.Interaction,
                     server_id: str = nextcord.SlashOption(required=True,
                                                           description="Server ID of the server you want to add.")
                     ):
    await interaction.response.defer(ephemeral=True)
    if owner_reject(interaction):
        return
    server_id = int(server_id)
    global servers, guilds_list
    if server_id not in guilds_list:
        await interaction.edit_original_message(content=f"Not a valid ID for a server I'm in.")
        return
    if server_info.server_exists(servers, server_id):
        await interaction.edit_original_message(content=f"Server already exists in the system. "
                                                        f"You can modify server attributes instead. "
                                                        f"<:sunnyy:1055107759231729735>")
        return

    servers.append(server_info.Server(server_id, 1, [], 1))
    server_info.write(servers)
    await interaction.edit_original_message(content=f"Server added.")


@commands.guild_only()
@client.slash_command(guild_ids=guilds_list, description="Deletes a server from the server file. Owner only.")
async def delete_server(interaction: nextcord.Interaction,
                        server_id: str = nextcord.SlashOption(required=True,
                                                              description="Server ID of the server you want to add.")
                        ):
    await interaction.response.defer(ephemeral=True)
    if owner_reject(interaction):
        return
    server_id = int(server_id)
    global servers, guilds_list
    if server_id not in guilds_list:
        await interaction.edit_original_message(content=f"Not a valid ID for a server I'm in.")
        return
    if not server_info.server_exists(servers, server_id):
        await interaction.edit_original_message(content=f"Server does not exist in the system.")
        return

    servers.remove(server_info.search_for_server(servers, server_id))
    server_info.write(servers)
    await interaction.edit_original_message(content=f"Server deleted.")


# Easter eggs I guess
@client.listen('on_message')
async def on_message(message):
    if message.author.bot:
        return
    if "qotd" in message.content.lower():
        await message.add_reaction("<:EeveeLurk:991271779735719976>")


if __name__ == "__main__":
    client.run(token)
