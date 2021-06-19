from starlette.requests import Request
from starlette.authentication import AuthenticationError
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
        username = data['username']
        password = data['password']
    except:
        raise AuthenticationError('Invalid authentication data in request')

    # check user authentication
    if username == request.app.state.VALID_USERNAME and password == request.app.state.VALID_PASSWORD:
        # create a JWT token and send to the user
        token = request.app.state.jwt.create_token(username)
        return ORJSONResponse(dict(token=token))
    else:
        raise AuthenticationError('Invalid username or password')
