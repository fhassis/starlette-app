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
        try:
            auth = request.headers['Authorization']
            scheme, token = auth.split()
            if scheme != 'Bearer':
                raise
            payload: Payload = request.app.state.jwt.validate_token(token)
        except TimeoutError:
            raise AuthenticationError('Token expired')
        except ValueError:
            raise AuthenticationError('Invalid token signature')
        except Exception:
            raise AuthenticationError('Invalid Authorization header')

        return AuthCredentials(['authenticated']), SimpleUser(payload['sub'])
