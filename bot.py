import interactions
from interactions import slash_command, SlashContext, CommandContext, Option, OptionType, listen
from interactions import ContextMenuContext, Message, message_context_menu
from secret import token, apikey
import requests

bot = interactions.Client()

def Is_A_Movie(name):
    header = {
        "accept": "application/json",
        "Authorization": apikey
        }
    url = f"https://api.themoviedb.org/3/search/movie?query={name}&language=en-US&page=1"
    response = requests.get(url, headers=header).json()
    return (response["total_results"] != 0, response)

def addToWatchList(id, typeS):
    header = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": apikey
    }
    url = "https://api.themoviedb.org/3/account/21924935/watchlist"
    data ={
        "media_type":typeS,
        "media_id": id,
        "watchlist": True
    }
    response = requests.post(url, json=data, headers=header).json()
    return response["success"]
@listen()
async def on_startup():
    print("Bot ready")

#! Need to add check if other content other than the movie name is in the message like a mention or etc...
@message_context_menu(name="Add movie to list")
async def addToListContext(ctx: ContextMenuContext):
    message: Message = ctx.target
    (status, json) = Is_A_Movie(message.content)
    if status:
        addToWatchList(json["results"][0]["id"], "Movie")
        await ctx.send(f"{message.content} has been added to the list")
    else:
        await ctx.send(f"{message.content} was not found to be a movie")


@slash_command(name="scan", description="will scan the channel for movies and shows")
async def scan(ctx: SlashContext):
    messages:list[str] = []
    if ctx.channel.message_count >= 50:
        await ctx.send("Sorry there is too many messages in this channel, you will need to add the movies or shows manually.")
    else:
        history = ctx.channel.history(limit=0)
        messages = history.flatten()
    
    if len(messages) > 0:
        for message in messages:
            temp:str = message.split("\n")
            for e in temp:
                (status, json) = Is_A_Movie(e)
                if status:
                    addToWatchList(json["results"][0]["id"], "Movie")
                else:
                    await ctx.send(f"{e} was not found to be a movie")
bot.start(token)