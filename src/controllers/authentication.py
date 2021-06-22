from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from orjson import loads

from src.utils.starlette import ORJSONResponse


async def login(request: Request):
    """
    Authenticates the user and returns a JWT token if successful.
    """
    try:
        # parses the request
        body: bytes = await request.body()
        data = loads(body)
    except:
        return PlainTextResponse('Invalid authentication data', HTTP_400_BAD_REQUEST)

    # check user authentication
    if data['username'] == request.app.state.VALID_USERNAME and data['password'] == request.app.state.VALID_PASSWORD:
        # create a JWT token and send to the user
        token = request.app.state.jwt.create_token(data['username'])
        return ORJSONResponse(dict(token=token))
    else:
        return PlainTextResponse('Invalid username or password', HTTP_401_UNAUTHORIZED)
