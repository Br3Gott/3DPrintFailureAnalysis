import subprocess
import json

import random

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

    # for _ws in connections:
        # await _ws.send_str('User joined!')
    print("User joined!")
    connections.append(ws)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                print(msg.data)
                # await ws.send_str('Hello client :D')
        elif msg.type == web.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
    
    connections.remove(ws)
    # for _ws in connections:
        # await _ws.send_str('User disconected!')
    print('websocket connection closed')

    return ws

async def sendMessage(title, msg):
    # print("Sending msg...")
    for _ws in connections:
        await _ws.send_str("{\"" + title + "\": " + json.dumps(msg) + "}")

async def getPs():
    p = subprocess.Popen(["ps", "aux" , "--sort=-pcpu"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['head', '-10'], stdin=p.stdout,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res = p2.stdout.read()
    resarr = res.decode("utf-8").split("\n")
    output = []
    resarr = resarr[1:]
    for line in resarr:
        inner = line.split(" ")
        clean_inner = []
        for elem in inner:
            if (len(elem) > 0):
                clean_inner.append(elem)
        output.append(clean_inner)
    prepared_output = []
    for line in output:
        if (len(line) > 0):
            temp = {}
            #user
            temp["user"] = line[0]
            #process id
            temp["processId"] = line[1]
            #cpu
            temp["cpu"] = line[2]
            #mem
            temp["memory"] = line[3]
            #start
            temp["start"] = line[8]
            #command + args
            command = line[10:]
            temp["command"] = " ".join(command)
            prepared_output.append(temp)
    return prepared_output

async def getDetectStatus():
    #filler for now
    output = {}
    dnn = {}
    dnn["success"] = random.randint(0,100)
    dnn["fail"] = 100 - dnn["success"]
    output["dnn"] = dnn
    cvs = {}
    cvs["difference"] = random.randint(0,100)
    output["cv"] = cvs

    return output

app = web.Application()
app.add_routes(routes)

async def wrapper():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

    while True:
        # await asyncio.sleep(5)
        # await sendMessage("regular", "Hello guys :/")
        await asyncio.sleep(5)
        ps = await getPs()
        await sendMessage("ps", ps)
        ov = await getDetectStatus()
        await sendMessage("ov", ov)

asyncio.run(wrapper())