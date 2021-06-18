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
        exp_time = int((datetime.now(timezone.utc) + timedelta(days=self.expiration_days)).timestamp())
        payload: Payload = dict(sub=username, exp=exp_time)
        b64_payload = urlsafe_b64encode(dumps(payload)).decode('utf-8')
        b64_signature = self._generate_signature(self.b64_header, b64_payload)
        return f'{self.b64_header}.{b64_payload}.{b64_signature}'

    def validate_token(self, token: str):
        b64_header, b64_payload, b64_signature = token.split('.')
        b64_signature_checker = self._generate_signature(b64_header, b64_payload)

        # load payload to check the field 'exp'
        payload: Payload = loads(urlsafe_b64decode(b64_payload))
        unix_time_now = datetime.now(timezone.utc).timestamp()

        if payload.get('exp') and payload['exp'] < unix_time_now:
            raise Exception('JWT Token Expired')

        if b64_signature_checker != b64_signature:
            raise Exception('JWT Token Invalid Signature')

        return payload

    def _generate_signature(self, b64_header: str, b64_payload: str):
        return urlsafe_b64encode(
            new(
                key=self.secret_key,
                msg=f'{b64_header}.{b64_payload}'.encode(),
                digestmod=sha256
            ).digest()
        ).decode('utf-8')


# if __name__ == '__main__':
#
#     username = 'someusername'
#     secret_key = '52d3f853c19f8b63c0918c126422aa2d99b1aef33ec63d41dea4fadf19406e54'
#
#     # create jwt object
#     jwt = JWT(secret_key)
#
#     # test token creation
#     token = jwt.create_token(username)
#     print(token)
#
#     # test token validation
#     decoded_token = jwt.validate_token(token)
#     print(decoded_token)
