from starlette.requests import Request
from starlette.authentication import AuthenticationBackend, AuthenticationError, SimpleUser, AuthCredentials

from src.services.jwt import Payload


class JwtAuthBackend(AuthenticationBackend):
    async def authenticate(self, request: Request):
        token = request.headers.get('token')
        if not token:
            token = request.query_params.get('token')
            if not token:
                return None
        try:
            payload: Payload = request.app.state.jwt.validate_token(token)
        except Exception as exc:
            raise AuthenticationError(str(exc))

        return AuthCredentials(['authenticated']), SimpleUser(payload['sub'])
