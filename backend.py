####################################################
# Name                                             #
# Backend Server                                   #
# Usage                                            #
# NOTE: First enter credentials in constants.py    #
# backend.py                                       #
#                                                  #
# Description                                      #
# Backend to do communication with the frontend.   #
#                                                  #
# Output / Function                                #
# Streams live preview, serves frontend and        #
# serves predictions and history.                  #
####################################################

import constants

import subprocess
import json

import random

import cv2 as cv
import base64
import time
import datetime

from picamera2 import Picamera2 as PiCamera
camera = PiCamera()
capture_config = camera.create_still_configuration(main={"format": 'RGB888', "size": (3280, 2464)})
camera.configure(capture_config)
camera.start()
time.sleep(1)

import asyncio
from aiohttp import web, MultipartWriter, ClientSession

from opencv.pre_processing.filter import filter_image
from opencv.pixel_observer.pixel import make_pixel
from tf.tensorflow_identify import Identify
import smtplib
from email.mime.text import MIMEText

async def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()

async def send_notification(receiver_email, message_text):
    await send_email("Octoprint Observer Notification", message_text, constants.sender_email, [receiver_email], constants.password)

routes = web.RouteTableDef()
routes.static('/assets', './frontend/dist/assets')

@routes.get('/')
async def static_content(request):
    return web.FileResponse('./frontend/dist/index.html')


@routes.get('/video')
async def mjpeg_handler(request):
    boundary = "boundarydonotcross"
    response = web.StreamResponse(status=200, reason='OK', headers={
        'Content-Type': 'multipart/x-mixed-replace; '
                        'boundary=--%s' % boundary,
    })
    await response.prepare(request)
    encode_param = (int(cv.IMWRITE_JPEG_QUALITY), 90)

    while True:
        frame = camera.capture_array("main")
        frame = cv.resize(frame, (640,480))
        with MultipartWriter('image/jpeg', boundary=boundary) as mpwriter:
            result, encimg = cv.imencode('.jpg', frame, encode_param)
            data = encimg.tobytes()
            mpwriter.append(data, {
                'Content-Type': 'image/jpeg'
            })
            try:
                await mpwriter.write(response, close_boundary=False)
            except:
                return response
        await asyncio.sleep(0.2)
    return response

connections = []
viewers = []

@routes.get('/ws')
async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    connections.append(ws)
    print('websocket connection opened, connected:{} viewers:{}'.format(len(connections), len(viewers)))

    # Initialize new client with current state
    await sendMessage("on", app["state"]["active"])
    await sendMessage("controlpanel", app["ctlpnl"])
    await sendMessage("email", app["ctlpnl"]["notification_email"])

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            elif msg.data == 'I want image :)':
                if ws not in viewers:
                    viewers.append(ws)
            elif msg.data == 'activate':
                app["state"]["active"] = True
                await sendMessage("on", app["state"]["active"])
                await send_notification(app["ctlpnl"]["notification_email"], 'Print monitoring has started!')
            elif msg.data == 'deactivate':
                app["state"]["active"] = False
                await sendMessage("on", app["state"]["active"])
            elif "allowedfails=" in msg.data:
                app["ctlpnl"]["allowedfails"] = int(msg.data[13:])
                await sendMessage("controlpanel", app["ctlpnl"])
            elif "historylength=" in msg.data:
                app["ctlpnl"]["historylength"] = int(msg.data[14:])
                await sendMessage("controlpanel", app["ctlpnl"])
            elif "email=" in msg.data:
                app["ctlpnl"]["notification_email"] = msg.data[6:]
                await sendMessage("email", app["ctlpnl"]["notification_email"])
                print("changed email:" + app["ctlpnl"]["notification_email"])
            else:
                print(msg.data)
        elif msg.type == web.WSMsgType.ERROR:
            print('websocket connection closed with exception %s' %
                  ws.exception())
    
    if ws in viewers:
        viewers.remove(ws)
    connections.remove(ws)
    print('websocket connection closed')

    return ws

async def sendMessage(title, msg):
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
    binary_image, masked_image = filter_image(image)
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

    while len(app["history_failed"]) >= app["ctlpnl"]["historylength"]:
        app["history_failed"].pop(0)
    
    if dnn["success"] < 50:
        app["history_failed"].append(True)

        if sum(app["history_failed"]) > app["ctlpnl"]["allowedfails"]:
            if app["state"]["active"] != False:
                app["state"]["active"] = False
                await sendMessage("on", app["state"]["active"])
                # send notification
                await send_notification(app["ctlpnl"]["notification_email"], 'Detected possible 3d printing failure. The current print has been paused. Please take action: http://10.8.160.203/')
                # await sendApp()
                await pausePrint()
    else:
        app["history_failed"].append(False)

    app["ctlpnl"]["currfails"] = sum(app["history_failed"])
    app["ctlpnl"]["currhistorylen"] = len(app["history_failed"])
    await sendMessage("controlpanel",  app["ctlpnl"])

    return output

async def captureImage():
    image = camera.capture_array("main")
    binary_image, masked_image = filter_image(image)
    raw_bytes = cv.imencode('.jpg', binary_image)[1].tobytes()

    # Record data to disk
    # curr_date = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    # cv.imwrite("./capture_data/{}.jpg".format(curr_date), image)

    for _ws in viewers:
        await _ws.send_bytes(raw_bytes)
    return image

async def pausePrint():
    headers = {'X-Api-Key': constants.octoprintkey} #API only localy accessible
    async with ClientSession(headers=headers) as session:
        payload = {
            "command": "pause",
            "action": "pause"
        }
        async with session.post('http://10.8.160.203/api/job', json=payload) as resp:
            print(resp.status)
            print(await resp.text())

app = web.Application()
app["state"] = {"active": False}
app["history_failed"] = []
app["ctlpnl"] = {
    "allowedfails": 3,
    "historylength": 5,
    "currfails": sum(app["history_failed"]),
    "currhistorylen": len(app["history_failed"]),
    "notification_email": "octoprintobserver@gmail.com"
}
app.add_routes(routes)

async def wrapper():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    pixel = make_pixel(0.4, 5)


    while True:
        await asyncio.sleep(2)
        ps = await getPs()
        await sendMessage("ps", ps)
        img = await captureImage()
        ov = await getDetectStatus(img, pixel)
        await sendMessage("ov", ov)

asyncio.run(wrapper())