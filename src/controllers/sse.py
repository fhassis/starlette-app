from starlette.requests import Request
from sse_starlette.sse import EventSourceResponse
from asyncio import CancelledError, Queue
from starlette.responses import PlainTextResponse


async def subscribe(request: Request):
    async def publish_data(msg_queue: Queue):
        try:
            while True:
                data = await msg_queue.get()
                yield data
        except CancelledError:
            print(f'Disconnected from client {request.client}')
    return EventSourceResponse(publish_data(request.app.state.msg_queue))


async def test_sse(request: Request):
    msg_queue: Queue = request.app.state.msg_queue
    await msg_queue.put('test sse message')
    return PlainTextResponse('')
