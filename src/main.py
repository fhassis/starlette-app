from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute
from starlette.config import Config
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from asyncio import Queue

from src.controllers import hello, login, sse, ws
from src.services.jwt import JWT
from src.utils.JwtAuthBackend import JwtAuthBackend


def startup():
    """
    Method executed as a callback on server startup.
    """
    # import configurations
    config = Config('config/app_config.env')

    # store valid user information in app state
    app.state.VALID_USERNAME = config.get('VALID_USERNAME')
    app.state.VALID_PASSWORD = config.get('VALID_PASSWORD')

    # stores JWT object in app state
    app.state.jwt = JWT(config.get('SECRET_KEY'), config.get('JWT_EXPIRATION_DAYS', cast=int))

    # creates a message queue
    app.state.msg_queue = Queue()


def shutdown():
    """
    Method executed as a callback on server shutdown.
    """
    pass


# defines the application routes
routes = [
    Route('/login', endpoint=login.login, methods=['POST']),
    Route('/hello', endpoint=hello.hello_user),
    Route('/sse', endpoint=sse.connect),
    Route('/test_sse', endpoint=sse.test_sse),
    WebSocketRoute('/ws', endpoint=ws.ws_handler)
]

# configures application middlewares
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
        expose_headers=['*']
    ),
    Middleware(AuthenticationMiddleware, backend=JwtAuthBackend()),
]

# creates the application
app = Starlette(
    routes=routes,
    middleware=middleware,
    on_startup=[startup],
    on_shutdown=[shutdown]
)
