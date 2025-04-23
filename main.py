from fastapi import FastAPI, Request

from RickAndMortyClient.client import RickAndMortyClient
from RickAndMortyClient.enums import CharacterGender, CharacterStatus

app = FastAPI()


@app.get("/character/{ids}")
async def characters_by_ids(request: Request, ids:str, export:bool=False):
    """ID can be one or multiple splitted by comma or list-like Example [1,2,3] or 1,2,3"""

    return RickAndMortyClient(request, export).get_characters_by_ids(ids)

@app.get("/location/{ids}")
async def characters_by_ids(request: Request, ids:str, export:bool=False):
    """ID can be one or multiple splitted by comma or list-like Example [1,2,3] or 1,2,3"""
    return RickAndMortyClient(request, export).get_characters_by_ids(ids)

@app.get("/episode/{ids}")
async def characters_by_ids(request: Request, ids:str, export:bool=False):
    """ID can be one or multiple splitted by comma or list-like Example [1,2,3] or 1,2,3"""
    return RickAndMortyClient(request, export).get_characters_by_ids(ids)

@app.get("/character")
async def characters(request: Request, name:str='',
                     status:CharacterStatus=None,
                     species:str='', character_type:str='',
                     gender:CharacterGender=None, page=1, export:bool=False):
    return RickAndMortyClient(request, export).get_characters(page=page, name=name, status=status, species=species,
                                                      character_type=character_type, gender=gender)


@app.get("/location")
async def locations(request: Request, name:str='', location_type:str='', dimension:str='', page=1, export:bool=False):

    return RickAndMortyClient(request, export).get_locations(page=page, name=name,
                                                     location_type=location_type, dimension=dimension,)

@app.get("/episode")
async def episodes(request: Request, name:str='', episode_code:str='', page=1, export:bool=False):

    return RickAndMortyClient(request, export).get_episodes(page=page, name=name, episode_code=episode_code)
