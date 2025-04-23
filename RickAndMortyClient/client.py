import io
import json
import re
from typing import Any
from urllib.parse import urlparse, urlencode

from fastapi import Request
from fastapi.responses import StreamingResponse
import requests
from starlette.responses import StreamingResponse

from settings import RICKANDMORTY_API_URL


def _process_urls(payload, new_url):
    """Replace Rick and Morty API endpoints with our App endpoints"""

    stoplist = ["image"]

    def replace_url(value, parent_key=None):
        if isinstance(value, str) and value.startswith(f"{RICKANDMORTY_API_URL}"):
            if parent_key in stoplist:
                return value
            return value.replace(f"{RICKANDMORTY_API_URL}", new_url)
        elif isinstance(value, list):
            return [replace_url(item, parent_key) for item in value]
        elif isinstance(value, dict):
            return {k: replace_url(v, k) for k, v in value.items()}
        else:
            return value

    return replace_url(payload)





class RickAndMortyClient:
    CHARACTERS_ENDPOINT = f"{RICKANDMORTY_API_URL}character"
    LOCATIONS_ENDPOINT = f"{RICKANDMORTY_API_URL}location"
    EPISODES_ENDPOINT = f"{RICKANDMORTY_API_URL}episode"

    def __init__(self, request: Request, export:bool=False):
        self.request = request
        self.export = export

    def _process_request(self, endpoint: str, params: dict = None, ids: str = None) -> StreamingResponse | dict[Any, Any]:
        if params is not None:
            filtered_params = {k: v for k, v in params.items() if v}
            query_string = urlencode(filtered_params)
            final_url = f"{endpoint}?{query_string}"
        elif ids is not None:
            final_url = f"{endpoint}/{ids}"
        else:
            raise ValueError("Either params or ids must be provided")

        response = requests.get(final_url).json()
        response = _process_urls(response, new_url='/')

        if self.export:
            """Multipage responses processing is omitted for simplification, hope that's fine"""

            json_data = json.dumps(response, indent=2)
            byte_stream = io.BytesIO(json_data.encode('utf-8'))
            return StreamingResponse(byte_stream, media_type="application/json", headers={
                "Content-Disposition": f"attachment; filename={final_url}.json"
            })
        else:
            return response

    def get_characters_by_ids(self, ids):
        return self._process_request(self.CHARACTERS_ENDPOINT, ids=ids)

    def get_locations_by_ids(self, ids):
        return self._process_request(self.LOCATIONS_ENDPOINT, ids=ids)

    def get_episodes_by_ids(self, ids):
        return self._process_request(self.EPISODES_ENDPOINT, ids=ids)

    def get_characters(self, page=1, name=None, status=None, species=None, character_type=None, gender=None):
        params = {
            "page": page,
            "name": name,
            "status": status.value if status else None,
            "species": species,
            "type": character_type,
            "gender": gender.value if gender else None
        }
        return self._process_request(self.CHARACTERS_ENDPOINT, params)

    def get_locations(self, page=1, name=None, location_type=None, dimension=None):
        params = {
            "page": page,
            "name": name,
            "type": location_type,
            "dimension": dimension,
        }

        return self._process_request(self.LOCATIONS_ENDPOINT, params)

    def get_episodes(self, page=1, name=None, episode_code=None):
        params = {
            "page": page,
            "name": name,
            "episode": episode_code,
        }

        return self._process_request(self.EPISODES_ENDPOINT, params)