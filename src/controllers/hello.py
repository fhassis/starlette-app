from starlette.requests import Request
from starlette.authentication import requires

from src.utils.starlette import ORJSONResponse


@requires('authenticated')
async def say_hello(request: Request):
    return ORJSONResponse({'msg': f'Hello {request.user.display_name}!'})
