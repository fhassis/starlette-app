from starlette.applications import Starlette
from starlette.routing import Route
from starlette.config import Config
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from src.controllers import hello, authentication
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
    Route('/', endpoint=hello.say_hello),
    Route('/login', endpoint=authentication.login, methods=['POST'])
]

# configures application middlewares
middleware = [
    Middleware(AuthenticationMiddleware, backend=JwtAuthBackend())
]

# creates the application
app = Starlette(
    routes=routes,
    middleware=middleware,
    on_startup=[startup],
    on_shutdown=[shutdown]
)
