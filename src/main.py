from starlette.applications import Starlette
from starlette.routing import Route
from starlette.config import Config

from src.controllers import hello, authentication
from src.utils.jwt import JWT


def startup():
    """
    Method executed as a callback on server startup.
    """
    print('Starting up server...')


def shutdown():
    """
    Method executed as a callback on server shutdown.
    """
    print('Shutting down server...')


# defines the application routes
routes = [
    Route('/', endpoint=hello.hello_world),
    Route('/authenticate', endpoint=authentication.authenticate, methods=['POST'])
]

# import configurations
config = Config('config/app_config.env')

# creates the application
app = Starlette(
    debug=config.get('DEBUG', cast=bool),
    routes=routes,
    on_startup=[startup],
    on_shutdown=[shutdown]
)

# store information in app state
app.state.config = config

# creates JWT object for authentication
app.state.jwt = JWT(config.get('SECRET_KEY'), config.get('JWT_EXPIRATION_DAYS', cast=int))

