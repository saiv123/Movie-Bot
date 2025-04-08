import interactions
from interactions import slash_command, SlashContext, slash_option, OptionType, listen
from interactions import ContextMenuContext, Message, message_context_menu
from interactions import Button, ButtonStyle, ActionRow
from interactions.api.events import Component
from secret import token, apikey
import requests

#? might want to have check return the id as well instead of searching the json

bot = interactions.Client()

#replace the current url api with this one url = "https://api.themoviedb.org/3/search/multi?query=namehere&language=en-US&page=1"
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
    url = f"https://api.themoviedb.org/3/search/multi?query={name}&language=en-US&page=1"
    response = requests.get(url, headers=header).json()
    if response["total_results"] != 0:
        media_type: str = response["results"][0]["media_type"]
        return (True, response, media_type)
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


if __name__ == "__main__":
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
            components = ActionRow(
                    Button(custom_id="yes", style=ButtonStyle.GREEN, label="Yes"),
                    Button(custom_id="no", style=ButtonStyle.RED, label="No")
                )
            await ctx.send(json["results"][0]["original_name"], components=components)
            try:
                used_component: Component = await bot.wait_for_component(components=components, timeout=30)
            except TimeoutError:
                await ctx.send("Timed out, run the command again to add the show or movie to the watchlist")
                return
            
            if used_component.ctx.custom_id == "yes":
                addToWatchList(json["results"][0]["id"], ty)
                await ctx.send(f"{json['results'][0]['original_name']} has been added to the watchlist")
            else:
                embed = interactions.Embed(title=f"List of the {'TV show' if ty == 'tv' else 'movie'}",description="List of the movies or shows that were found use add with id command to add them to the watchlist", images=json)
                for i in json["results"]:
                    embed.add_field(name="Title", value=f"{i['original_name']} - {str(i['id'])}")
                await ctx.send(embeds=embed)
        else:
            await ctx.send(f"{name} was not found to be a movie or TV show")

    @slash_command(name="add_with_id", description="Add a movie or TV show to the watchlist with id")
    @slash_option(
        name="id",
        description="ID of the movie or TV show",
        required=True,
        opt_type=OptionType.INTEGER
    )
    async def add_with_id(ctx: SlashContext, id: int):
        headers = {
            "accept": "application/json",
            "Authorization": apikey
        }
        
        # Check if the ID corresponds to a TV show
        tv_url = f"https://api.themoviedb.org/3/tv/{id}?language=en-US"
        tv_response: dict = requests.get(tv_url, headers=headers).json()
        
        if "id" in tv_response:
            media_type = "tv"
            if addToWatchList(id, media_type):
                await ctx.send(f"{tv_response['name']} has been added to the watchlist")
        
        # Check if the ID corresponds to a movie
        movie_url = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"
        movie_response = requests.get(movie_url, headers=headers).json()
        
        if "id" in movie_response:
            media_type = "movie"
            if addToWatchList(id, media_type):
                await ctx.send(f"{movie_response['title']} has been added to the watchlist")
        else:
            await ctx.send(f"Movie or TV show with ID {id} not found")
    bot.start(token)