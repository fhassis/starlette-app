from starlette.requests import Request
from starlette.authentication import requires

from src.utils.ORJSONResponse import ORJSONResponse


@requires('authenticated')
async def hello_user(request: Request):
    return ORJSONResponse({'msg': f'Hello {request.user.display_name}!'})
