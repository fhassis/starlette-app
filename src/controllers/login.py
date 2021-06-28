from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from orjson import loads


async def login(request: Request):
    """
    Authenticates the user and returns a JWT token if successful.
    """
    body: bytes = await request.body()
    try:
        data = loads(body)
        username = data['username']
        password = data['password']
    except:
        return PlainTextResponse('Invalid authentication data', HTTP_400_BAD_REQUEST)

    # check user authentication
    if username == request.app.state.VALID_USERNAME and password == request.app.state.VALID_PASSWORD:
        # create a JWT token and send to the user
        token = request.app.state.jwt.create_token(data['username'])
        return PlainTextResponse(token)
    else:
        return PlainTextResponse('Invalid username or password', HTTP_401_UNAUTHORIZED)
