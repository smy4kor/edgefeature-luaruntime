import json

class Artifacts:
    def __init__(self,name,url):
        self.name = name
        self.url = url

class SoftwareModules:
    def __init__(self,name,version,artifacts):
        self.name = name
        self.version = version
        self.artifacts = artifacts
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class DittoCommand:
    def __init__(self, mqttPayloadStr):
        payload = json.loads(mqttPayloadStr)
        self.payload = payload
        self.topic = payload['topic']
        self.path = payload['path']
        self.dittoCorrelationId = payload['headers']["correlation-id"]
    def isSoftwareUpdate(self):
        return (self.isInstallCommand() or self.isDownloadCommand())
    def isInstallCommand(self):
        return self.path.endswith('install')
    def isDownloadCommand(self):
        return self.path.endswith('download')
    def print(self):
        myorder = "Topic is {}, path is {}, dittoCorrelationId is {}."
        print(myorder.format(self.topic, self.path, self.dittoCorrelationId))
        print(self.payload)
    def getSoftwareModules(self):
        lst = []
        if 'value' not in self.payload.keys():
            return []
        
        for swMod in self.payload['value']['softwareModules']: 
            name = swMod['softwareModule']['name']
            vrsn = swMod['softwareModule']['version']
            arts = []
            for artifact in swMod['artifacts']:
             arts.append(Artifacts(artifact['filename'], artifact['download']['HTTPS']['url']))
            lst.append(SoftwareModules(name,vrsn,arts))
        return lst

