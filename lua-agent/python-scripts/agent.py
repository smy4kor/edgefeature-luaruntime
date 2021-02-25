import os
import os.path
import json
from json import JSONEncoder
import uuid


class Agent:

    def __init__(self, name, version, type):
        self.name = name
        self.version = version
        self.type = type
        self.featureId = ""
        self.check()

    def check(self):
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
    
