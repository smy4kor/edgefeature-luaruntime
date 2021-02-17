#!/usr/bin/python3
import paho.mqtt.client as mqtt
import time
import json
from commands import DittoCommand
from subscriptioninfo import SubscriptionInfo
from downloader import DownloadManager

sInfo = SubscriptionInfo()
DEVICE_INFO_TOPIC = "edge/thing/response"
MQTT_TOPIC = [(DEVICE_INFO_TOPIC,0),("command///req/#",0)]

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing to a topic that sends install or download command
    client.subscribe(MQTT_TOPIC)
    # hint: to register as agent or operation status, use "e".

# The callback when a install or download command is received
# msg is of type MQTTMessage
def on_message(client, userdata, msg):
    # try-catch will ensure that subscription is not broken in case of exception.
    try:
        processEvent(msg)
    except Exception as err:
        print(err)


def processEvent(msg):
    payloadStr = str(msg.payload.decode("utf-8", "ignore"))
    payload = json.loads(payloadStr)
    if msg.topic == DEVICE_INFO_TOPIC:
        sInfo.compute(payload)
    else:
        handleSupEvent(msg,payload)
        aknowledge()

def handleSupEvent(msg,payload):
    print("message topic is" + msg.topic)
    cmd = DittoCommand(payload,msg.topic)
    print('Is install command: ' + str(cmd.isInstallCommand()));
    print('Is software updatable command: ' + str(cmd.isSoftwareUpdate()));
    if cmd.isInstallCommand() and cmd.isSoftwareUpdate():
        print("request id is: " + str(cmd.getRequestId()))
        print('Parsing software module information')
        for swMod in cmd.getSoftwareModules():
            print(swMod.toJson())
            for art in swMod.artifacts:
                DownloadManager().download(art)

                 
def aknowledge():
    print("Sending confirmation for tenant: " + sInfo.hubTenantId)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
