from starlette.websockets import WebSocket, WebSocketDisconnect
from starlette.authentication import requires


@requires('authenticated')
async def ws_handler(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            msg = await websocket.receive_text()
            if msg == 'close':
                break
            await websocket.send_text('echoed: ' + msg)
    except WebSocketDisconnect as d:
        if d.code == 1000:
            print('Disconnected. code %s', d.code)
        else:
            print('Disconnected. code %s', d.code)
    else:
        await websocket.close()
