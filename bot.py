import interactions
from interactions import slash_command, SlashContext, slash_option, OptionType, listen
from interactions import ContextMenuContext, Message, message_context_menu
from interactions import Button, ButtonStyle, ActionRow
from interactions.api.events import Component
from secret import token, apikey
import requests

#? might want to have check return the id as well instead of searching the json

bot = interactions.Client()

def Check(name: str) -> tuple[bool, dict | None, str | None]:
    """
    A Function that checks the name of a movie or tv show
    
    Args:
        name: string
    Returns:
        Tuple (bool, dict , str): if nothing is found returns (False, None, None)
    """
    header = {
        "accept": "application/json",
        "Authorization": apikey
        }
    types = ["movie", "tv"]
    for Type in types:
        url = f"https://api.themoviedb.org/3/search/{Type}?query={name}&language=en-US&page=1"
        response = requests.get(url, headers=header).json()
        if response["total_results"] != 0 :
            return (response["total_results"] != 0, response, Type)
    return (False, None, None)

def addToWatchList(id:int, typeS:str)->bool:
    """
    A Function to add a movie or tv show to "The movie db" watchlist

    Args:
        id: integer usually from check function
        typeS: type of the id usually from the check function
    
    Returns:
        Boolean
    """
    header = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": apikey
    }
    url = "https://api.themoviedb.org/3/account/21924935/watchlist"
    data ={
        "media_type":typeS.lower(),
        "media_id": id,
        "watchlist": True
    }
    response = requests.post(url, json=data, headers=header).json()
    return response["success"]

def ButtonCheck(component: Component)->bool:
    if component.ctx.custom_id == "yes":
        return True
    return False

@listen()
async def on_startup():
    print("Bot ready")

@message_context_menu(name="Add movie to list")
async def addToListContext(ctx: ContextMenuContext):
    message: Message = ctx.target
    (status, json, ty) = Check(message.content)
    if status:
        addToWatchList(json["results"][0]["id"], ty)
        await ctx.send(f"{message.content} has been added to the list")
    else:
        await ctx.send(f"{message.content} was not found to be a movie\nIf there is multiple names in one message I can't process that yet ;(")

@slash_command(name="add_to_watchlist", description="Add a movie or TV show to the watchlist")
@slash_option(
    name="name",
    description="Name of the movie or TV show",
    required=True,
    opt_type=OptionType.STRING
)
async def add_to_watchlist(ctx: SlashContext, name: str):
    (status, json, ty) = Check(name)
    if status:
        if json["total_results"]:
            components = ActionRow(
                Button(custom_id="yes", style=ButtonStyle.GREEN, label="Yes"),
                Button(custom_id="no", style=ButtonStyle.RED, label="No")
            )

            await ctx.send(json["results"][0]["original_name"], components=components)
            try:
                used_component: Component = await bot.wait_for_component(components=components, check=ButtonCheck(), timeout=30)
            except TimeoutError:
                await ctx.send("Timed out, run the command again to add the show or movie to the watchlist")
        if used_component.ctx.custom_id == "yes":
            addToWatchList(json["results"][0]["id"], ty)
            await ctx.send(f"{name} has been added to the watchlist")
        else:
            await ctx.send(f"{name} was not added to the watchlist")
    else:
        await ctx.send(f"{name} was not found to be a movie or TV show")
##Command deprecated, will only allow the right click and add or with sending a message in a channel specified
# @slash_command(name="scan", description="will scan the channel for movies and shows")
# async def scan(ctx: SlashContext):
#     messages:list[str] = []
#     if ctx.channel.message_count >= 50:
#         await ctx.send("Sorry there is too many messages in this channel, you will need to add the movies or shows manually.")
#     else:
#         history = ctx.channel.history(limit=0)
#         messages = history.flatten()
    
#     if len(messages) > 0:
#         for message in messages:
#             temp:str = message.split("\n")
#             for e in temp:
#                 (status, json) = Is_A_Movie(e)
#                 if status:
#                     addToWatchList(json["results"][0]["id"], "movie")
#                 else:
#                     await ctx.send(f"{e} was not found to be a movie")
bot.start(token)