from starlette.responses import Response
import typing
from orjson import dumps


class ORJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return dumps(content)
