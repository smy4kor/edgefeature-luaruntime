#!/usr/bin/python3
import paho.mqtt.client as mqtt
import time
import json
from commands import DittoCommand
from subscriptioninfo import SubscriptionInfo
from downloader import DownloadManager
from dittoresponse import DittoResponse

sInfo = SubscriptionInfo()
DEVICE_INFO_TOPIC = "edge/thing/response"
MQTT_TOPIC = [(DEVICE_INFO_TOPIC, 0), ("command///req/#", 0)]


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing to a topic that sends install or download command
    client.subscribe(MQTT_TOPIC)
    # hint: to register as agent or operation status, use "e".

def on_publish(client,userdata,result):
    print("data published: " + str(result))

# The callback when a install or download command is received
# msg is of type MQTTMessage
def on_message(client, userdata, msg):
    # try-catch will ensure that subscription is not broken in case of exception.
    try:
        processEvent(msg)
    except Exception as err:
        print(err)


def processEvent(msg):
    '''Will process the mqtt message based on the use case. Usecase is determined by the message topic.'''
    payloadStr = str(msg.payload.decode("utf-8", "ignore"))
    payload = json.loads(payloadStr)
    if msg.topic == DEVICE_INFO_TOPIC:
        sInfo.compute(payload)
    else:
        cmd = DittoCommand(payload, msg.topic)
        handleSupEvent(cmd)

def handleSupEvent(cmd):
    cmd.printInfo()
    aknowledge(cmd)
    if cmd.isInstallCommand() and cmd.isSoftwareUpdate():
        updateSupFeature(cmd,"STARTED", "Received the request on the device.")
        print("request id is: " + str(cmd.getRequestId()))
        print("")
        # print('Parsing software module information')
        for swMod in cmd.getSoftwareModules():
            # print(swMod.toJson())
            for art in swMod.artifacts:
                updateSupFeature(cmd,"DOWNLOADING", "Downloading " + art.name)
                DownloadManager().download(art)
                updateSupFeature(cmd,"DOWNLOADED", "Downloaded " + art.name)
            updateSupFeature(cmd, "FINISHED_SUCCESS", "Completed installing " + swMod.name)

# https://vorto.eclipseprojects.io/#/details/org.eclipse.hawkbit:Status:2.0.0
def updateSupFeature(cmd,status,message):
    print(">>> sending sup update " + status + " with message: " + message)
    pth = "/features/" + cmd.featureId + "/properties/status/lastOperation"
    rsp = DittoResponse("com.peter2/aa-machine-1/things/twin/commands/modify",pth,None)
    rsp.prepareSupResponse(cmd,status,message)
    if status == "FINISHED_SUCCESS":
        print(rsp.toJson())
        print("======== Done =============")
    client.publish("e",rsp.toJson())

        
def aknowledge(cmd):
    status = 200
    mosquittoTopic = "command///res/" + str(cmd.getRequestId()) + "/" + str(status)
    print("======== Sending aknowledgement for ditto requestId: %s =============" %(cmd.getRequestId()))
    aknPath = cmd.path.replace("inbox","outbox") ## "/features/manually-created-lua-agent/outbox/messages/install"
    rsp = DittoResponse(cmd.dittoTopic,aknPath,status)
    rsp.prepareAknowledgement(cmd.dittoCorrelationId)
    print(rsp.toJson())
    client.publish(mosquittoTopic,rsp.toJson())
    print("======== Done: Aknowledgement sent on topic %s =============" %(mosquittoTopic))


client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
