import os
import os.path
import json
from json import JSONEncoder
import uuid
from dittoresponse import DittoResponse

class Agent:

    def __init__(self, name, version, type,featureId):
        self.name = name
        self.version = version
        self.type = type
        self.featureId = featureId
        # self.generateRandomIdAndCache()

    def generateRandomIdAndCache(self):
        # generate a feature id and cache it locally so that it can be later detected.
        filePath = self.getCachePath()
        if os.path.isfile(filePath):
            f = open(filePath, "r")
            self.featureId = json.loads(f.read())["featureId"]
            f.close()
            print ("Agent cache exist with feature id",self.featureId)
        else:
            self.featureId = str(uuid.uuid4())
            f = open(filePath,"w+")
            f.writelines(self.toJson())
            f.close()
            print ("Created agent cache with feature id",self.featureId)

    def getCachePath(self):
        dir = os.getcwd() + "/agent-feature-cache/"
        if os.path.isdir(dir) == False:
            os.mkdir(dir)
        return os.getcwd() + "/agent-feature-cache/" + self.name + ":" + self.version + ".json"

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    def register(self,mqttClient,subscriptionInfo):
        dittoRspTopic = "{}/{}/things/twin/commands/modify".format(subscriptionInfo.namespace, subscriptionInfo.deviceId)
        value = {}
        value["definition"] = ["org.eclipse.hawkbit.swupdatable:SoftwareUpdatable:2.0.0"]
        value["properties"] = {}
        value["properties"]["status"]= {
            "agentName": self.name,
            "agentVersion": self.version,
            "softwareModuleType": self.type
        }
        path = "/features/" + self.featureId
        rsp = DittoResponse(dittoRspTopic, path, None)
        
        rsp.value = value
        mqttClient.publish("e", rsp.toJson(), qos=1)
