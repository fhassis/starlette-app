from starlette.applications import Starlette
from starlette.routing import Route
from starlette.config import Config
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.controllers import hello, authentication, sse
from src.utils.jwt import JWT
from src.utils.starlette import JwtAuthBackend


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


def shutdown():
    """
    Method executed as a callback on server shutdown.
    """
    pass


# defines the application routes
routes = [
    Route('/login', endpoint=authentication.login, methods=['POST']),
    Route('/', endpoint=hello.say_hello),
    Route('/sse', endpoint=sse.subscribe)
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
