import time
import asyncio
from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.FileResponse('./index.html')

connections = []

@routes.get('/ws')
async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    for _ws in connections:
        await _ws.send_str('User joined!')
        print("User joined!")
    connections.append(ws)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                print(msg.data)
                await ws.send_str('Hello client :D')
        elif msg.type == web.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
    
    connections.remove(ws)
    for _ws in connections:
        await _ws.send_str('User disconected!')
    print('websocket connection closed')

    return ws

async def sendMessage(msg):
    while True:
        time.sleep(1)
        print("Running...")
        for _ws in connections:
            await _ws.send_str(msg)

app = web.Application()
app.add_routes(routes)

async def wrapper():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

    while True:
        await asyncio.sleep(10)
        await sendMessage("Hello guys :/")

asyncio.run(wrapper())


