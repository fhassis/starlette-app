from hmac import new
from hashlib import sha256
from datetime import datetime, timezone, timedelta
from base64 import urlsafe_b64encode, urlsafe_b64decode
from orjson import loads, dumps
from typing import TypedDict


class Payload(TypedDict):
    sub: str    # subject: username
    exp: int    # expiration time, in UTC unix time


class JWT(object):
    """
    Implements JWT tokens using HS256 algorithm.
    """
    secret_key: bytes
    expiration_days: int
    b64_header: str

    def __init__(self, secret_key: str, expiration_days: int):
        self.secret_key = secret_key.encode()
        self.expiration_days = expiration_days
        self.b64_header = urlsafe_b64encode(dumps({'typ': 'JWT', 'alg': 'HS256'})).decode('utf-8')

    def create_token(self, username: str) -> str:
        """
        Creates a JWT token with the payload type "Payload".
        """
        exp_time = int((datetime.now(timezone.utc) + timedelta(days=self.expiration_days)).timestamp())
        payload: Payload = dict(sub=username, exp=exp_time)
        b64_payload = urlsafe_b64encode(dumps(payload)).decode('utf-8')
        b64_signature = self._generate_signature(self.b64_header, b64_payload)
        return f'{self.b64_header}.{b64_payload}.{b64_signature}'

    def validate_token(self, token: str) -> Payload:
        """
        Validates a given JWT token and returns its payload if successful.
        """
        # parses the token to be validated
        b64_header, b64_payload, b64_signature = token.split('.')

        # load the payload as json
        payload = loads(urlsafe_b64decode(b64_payload))

        # check the token expiration time
        if payload.get('exp') and payload['exp'] < datetime.now(timezone.utc).timestamp():
            raise Exception('JWT Token Expired')

        # check the token signature
        if b64_signature != self._generate_signature(b64_header, b64_payload):
            raise Exception('JWT Token Invalid Signature')

        return payload

    def _generate_signature(self, b64_header: str, b64_payload: str) -> str:
        return urlsafe_b64encode(
            new(
                key=self.secret_key,
                msg=f'{b64_header}.{b64_payload}'.encode(),
                digestmod=sha256
            ).digest()
        ).decode('utf-8')
