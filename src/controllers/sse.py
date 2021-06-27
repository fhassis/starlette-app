from starlette.requests import Request
from sse_starlette.sse import EventSourceResponse
from asyncio import sleep, CancelledError


async def subscribe(request: Request):
    async def publish_data():
        counter = 0
        try:
            while True:
                yield dict(data=counter)
                counter += 1
                await sleep(5)
        except CancelledError:
            print(f'Disconnected from client (via refresh/close) {request.client}')
    return EventSourceResponse(publish_data())
