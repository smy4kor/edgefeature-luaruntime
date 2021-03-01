#!/usr/bin/python3
import paho.mqtt.client as mqtt
import time
import json
from commands import DittoCommand
from subscriptioninfo import SubscriptionInfo
from downloader import DownloadManager
from executor import ScriptExecutor
from dittoresponse import DittoResponse
from agent import Agent
from softwareFeatureCache import SoftwareFeatureCache

agent = Agent("script", "2.0.0", "script", 'software-updatable-script-agent')
sInfo = SubscriptionInfo()
DEVICE_INFO_TOPIC = "edge/thing/response"
MQTT_TOPIC = [(DEVICE_INFO_TOPIC, 0), ("command///req/#", 0)]


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing to a topic that sends install or download command
    client.subscribe(MQTT_TOPIC)
    # hint: to register as agent or operation status, use "e".


def on_publish(client, userdata, result):
    print("data published: " + str(result))


# The callback when a install or download command is received
# msg is of type MQTTMessage
def on_message(client, userdata, msg):
    print("received message on mqtt topic: " + msg.topic)
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
        agent.register(client, sInfo)
    elif msg.topic == "THING_REQUEST_TOPIC":
        print("all features are \n", payload)
    else:
        cmd = DittoCommand(payload, msg.topic)
        handleSupEvent(cmd)

    
def handleSupEvent(cmd):
    # cmd.printInfo()
    if cmd.isInstallCommand() and cmd.isSoftwareUpdate() and cmd.featureId == agent.featureId:
        print("processing rollouts request with ditto req id: " + str(cmd.getRequestId()))
        aknowledge(cmd)
        handleRolloutRequest(cmd)
    elif SoftwareFeatureCache.hasCache(cmd.featureId):
        print("Need to re-execute " + cmd.featureId)
        aknowledge(cmd)
        reExecuteSoftware(cmd.featureId)
    else:
        print("command received on unknown feature: " + str(cmd.featureId))   
        # else, from cache file stored with cmd.featureId and execute the scripts stored there

def reExecuteSoftware(featureId):
    swCache = SoftwareFeatureCache.loadOrCreate(featureId);
    execResult = ""
    for file in swCache.files:
        execResult += ScriptExecutor().executeFile(file) + "\n"
    swCache.createDittoFeature(client, sInfo, execResult)

def handleRolloutRequest(cmd):
    print("Rollouts correlationId is: " + str(cmd.getRolloutsCorrelationId()))
    # print('Parsing software module information')
    for swMod in cmd.getSoftwareModules():
        execResult = ""
        featureId = swMod.name.replace(":", "-") + "-" + swMod.version
        swCache = SoftwareFeatureCache.loadOrCreate(featureId);
        # print(swMod.toJson())
        for art in swMod.artifacts:
            updateSupFeature(cmd, "DOWNLOADING", "Downloading " + art.name, swMod)
            filePath = DownloadManager().download(art)
            swCache.files.append(filePath)
            updateSupFeature(cmd, "DOWNLOADED", "Downloaded " + art.name, swMod)
            # # https://vorto.eclipseprojects.io/#/details/vorto.private.test:Executor:1.0.0
            updateSupFeature(cmd, "INSTALLING", "Executing lua script: " + filePath, swMod)
            res = ScriptExecutor().executeFile(filePath) + "\n"
            updateSupFeature(cmd, "INSTALLED", execResult, swMod)
            execResult += res
        swCache.save()
        swCache.createDittoFeature(client, sInfo, execResult)
        updateSupFeature(cmd, "FINISHED_SUCCESS", execResult, swMod)   

    
# https://vorto.eclipseprojects.io/#/details/org.eclipse.hawkbit:Status:2.0.0
def updateSupFeature(cmd, status, message, swModule=None):
    print(">>> sending sup update " + status + " with message: " + message)
    pth = "/features/{}/properties/status/lastOperation".format(cmd.featureId)
    
    dittoRspTopic = "{}/{}/things/twin/commands/modify".format(sInfo.namespace, sInfo.deviceId)
    rsp = DittoResponse(dittoRspTopic, pth, None)
    rsp.prepareSupResponse(cmd.getRolloutsCorrelationId(), status, message, swModule)
    if status == "FINISHED_SUCCESS":
        print(rsp.toJson())
        print("======== Done =============")
    client.publish("e", rsp.toJson(), qos=1)

        
def aknowledge(cmd):
    status = 200
    mosquittoTopic = "command///res/" + str(cmd.getRequestId()) + "/" + str(status)
    # print("======== Sending aknowledgement for ditto requestId: %s =============" %(cmd.getRequestId()))
    aknPath = cmd.path.replace("inbox", "outbox")  # # "/features/manually-created-lua-agent/outbox/messages/install"
    rsp = DittoResponse(cmd.dittoTopic, aknPath, status)
    rsp.prepareAknowledgement(cmd.dittoCorrelationId)
    # print(rsp.toJson())
    client.publish(mosquittoTopic, rsp.toJson())
    print("======== Aknowledgement sent on topic " + mosquittoTopic + " =============")


client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
