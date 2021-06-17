from starlette.applications import Starlette
from starlette.routing import Route

from src.controllers import hello


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
    Route('/', hello.hello_world)
]

# creates the application
app = Starlette(
    routes=routes,
    on_startup=[startup],
    on_shutdown=[shutdown]
)
