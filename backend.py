import subprocess
import json

import random

import cv2 as cv
import base64
import time

from picamera2 import Picamera2 as PiCamera
camera = PiCamera()
capture_config = camera.create_still_configuration(main={"format": 'RGB888', "size": (3280, 2464)})
camera.configure(capture_config)
camera.start()
time.sleep(1)

import asyncio
from aiohttp import web

from opencv.pre_processing.filter import filter_image
from opencv.pixel_observer.pixel import make_pixel
from tensorflow.tensorflow_identify import Identify

routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.FileResponse('./index.html')

connections = []
viewers = []

@routes.get('/ws')
async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # for _ws in connections:
        # await _ws.send_str('User joined!')
    connections.append(ws)
    print('websocket connection opened')

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            elif msg.data == 'I want image :)':
                if ws not in viewers:
                    viewers.append(ws)
            else:
                print(msg.data)
                # await ws.send_str('Hello client :D')
        elif msg.type == web.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
    
    if ws in viewers:
        viewers.remove(ws)

    connections.remove(ws)
    # for _ws in connections:
        # await _ws.send_str('User disconected!')
    print('websocket connection closed, conn:' + str(len(connections)) + ' viewers:' + str(len(viewers)))

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

async def getDetectStatus(image, pixel):
    #filler for now
    binary_image = filter_image(image)
    tf_image = cv.cvtColor(binary_image, cv.COLOR_GRAY2RGB)
    ident = Identify.run(tf_image, verbose=False)
    
    
    validity, difference = pixel.add(binary_image)
    # if not validity == None:
    #     if not validity:
    #         display_text += "Pixel count failure! [{:.2f}]".format(difference) + "\n"
    #     else:
    #         display_text += "Pixel count is valid! [{:.2f}]".format(difference) + "\n"
    # display_text += pixel.history_fitting() + "\n"
    output = {}
    dnn = {}
    dnn["success"] = ident[1]
    dnn["fail"] = ident[0]
    output["dnn"] = dnn
    cvs = {}
    cvs["difference"] = difference
    output["cv"] = cvs

    return output

async def captureImage():
    image = camera.capture_array("main")
    # width = 640
    # height = 480
    # image = cv.resize(image, (width, height), interpolation = cv.INTER_AREA)
    binary_image = filter_image(image)
    raw_bytes = cv.imencode('.jpg', binary_image)[1].tobytes()


    for _ws in viewers:
        await _ws.send_bytes(raw_bytes)
    return image

app = web.Application()
app.add_routes(routes)

async def wrapper():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    pixel = make_pixel(0.4, 5)

    while True:
        # await asyncio.sleep(5)
        # await sendMessage("regular", "Hello guys :/")
        await asyncio.sleep(2)
        ps = await getPs()
        await sendMessage("ps", ps)
        img = await captureImage()
        ov = await getDetectStatus(img, pixel)
        await sendMessage("ov", ov)

asyncio.run(wrapper())