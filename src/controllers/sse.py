from starlette.requests import Request
from starlette.authentication import requires
from sse_starlette.sse import EventSourceResponse
from asyncio import CancelledError, Queue
from starlette.responses import PlainTextResponse


@requires('authenticated')
async def connect(request: Request):
    async def send_data(msg_queue: Queue):
        try:
            while True:
                data = await msg_queue.get()
                yield data
        except CancelledError:
            print(f'Disconnected from client {request.client}')
    return EventSourceResponse(send_data(request.app.state.msg_queue))


@requires('authenticated')
async def test_sse(request: Request):
    msg = request.query_params.get('msg', 'test sse message')
    msg_queue: Queue = request.app.state.msg_queue
    await msg_queue.put(msg)
    return PlainTextResponse('')
