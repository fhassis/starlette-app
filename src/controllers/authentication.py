from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from orjson import loads

from src.utils.starlette import ORJSONResponse


async def authenticate(request: Request):
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
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='invalid authentication data in request')

    # check user authentication
    if username == request.app.state.VALID_USERNAME and password == request.app.state.VALID_PASSWORD:
        token = request.app.state.jwt.create_token(username)
        return ORJSONResponse(dict(token=token))
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='invalid username or password')
