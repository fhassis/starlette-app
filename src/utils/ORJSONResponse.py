from starlette.responses import Response
from orjson import dumps


class ORJSONResponse(Response):
    media_type = 'application/json'

    def render(self, content: dict) -> bytes:
        return dumps(content)
