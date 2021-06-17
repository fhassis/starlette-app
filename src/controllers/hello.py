from starlette.requests import Request

from src.utils.starlette import ORJSONResponse


async def hello_world(request: Request):
    return ORJSONResponse({'hello': 'World!'})
