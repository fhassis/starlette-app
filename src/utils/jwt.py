import hmac
from hashlib import sha256
from datetime import datetime, timedelta
from base64 import urlsafe_b64encode, urlsafe_b64decode
from orjson import loads, dumps
from typing import Any


class JWT(object):
    """
    Implements JWT tokens using HS256 algorithm.
    """
    secret_key: bytes
    b64_header: bytes

    def __init__(self, secret_key: str):
        self.secret_key = secret_key.encode()
        self.b64_header = urlsafe_b64encode(dumps({'typ': 'JWT', 'alg': 'HS256'}))

    def create_token(self, payload: Any):
        b64_payload: bytes = urlsafe_b64encode(dumps(payload))
        signature = hmac.new(
            key=self.secret_key,
            msg=f'{self.b64_header.decode()}.{b64_payload.decode()}'.encode(),
            digestmod=sha256
        ).digest()
        return f'{self.b64_header.decode()}.{b64_payload.decode()}.{urlsafe_b64encode(signature).decode()}'

    def validate_token(self, token: str):
        b64_header, b64_payload, b64_signature = token.split('.')
        b64_signature_checker = urlsafe_b64encode(
            hmac.new(
                key=self.secret_key,
                msg=f'{b64_header}.{b64_payload}'.encode(),
                digestmod=sha256
            ).digest()
        ).decode()

        # payload extraido antes para checar o campo 'exp'
        payload = loads(urlsafe_b64decode(b64_payload))
        unix_time_now = datetime.now().timestamp()

        if payload.get('exp') and payload['exp'] < unix_time_now:
            raise Exception('Token expirado')

        if b64_signature_checker != b64_signature:
            raise Exception('Assinatura inválida')

        return payload


if __name__ == '__main__':

    from jwt_original import create_jwt, verify_and_decode_jwt

    payload = {
        'userId': '55395427-265a-4166-ac93-da6879edb57a',
        'exp': (datetime.now() + timedelta(minutes=5)).timestamp(),
    }
    jwt_created = create_jwt(payload)
    print(jwt_created)
    decoded_jwt = verify_and_decode_jwt(jwt_created)
    print(decoded_jwt)

    print('-------------------------')

    jwt = JWT('52d3f853c19f8b63c0918c126422aa2d99b1aef33ec63d41dea4fadf19406e54')
    token = jwt.create_token(payload)
    print(token)
    decoded_token = jwt.validate_token(token)
    print(decoded_token)
