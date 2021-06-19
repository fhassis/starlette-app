from starlette.responses import Response
from starlette.requests import Request
from starlette.authentication import AuthenticationBackend, AuthenticationError, SimpleUser, AuthCredentials
from orjson import dumps

from src.utils.jwt import Payload


class ORJSONResponse(Response):
    media_type = 'application/json'

    def render(self, content: dict) -> bytes:
        return dumps(content)


class JwtAuthBackend(AuthenticationBackend):
    async def authenticate(self, request: Request):

        if 'Authorization' not in request.headers:
            return
        auth = request.headers['Authorization']

        try:
            scheme, token = auth.split()
            if scheme != 'Bearer':
                return
            payload: Payload = request.app.state.jwt.validate_token(token)
        except:
            raise AuthenticationError('Invalid authentication token')

        return AuthCredentials(['authenticated']), SimpleUser(payload['sub'])
