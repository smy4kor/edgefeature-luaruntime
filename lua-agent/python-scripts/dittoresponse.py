import json

class DittoResponse:
    def __init__(self,topic,path,responseCode):
        self.topic = topic
        self.path = path.replace("inbox","outbox") ## "/features/manually-created-lua-agent/outbox/messages/install"
        
        if responseCode:
            self.status = responseCode

    def prepareAknowledgement(self,dittoCorrelationId):
        self.value = {}
        self.headers = {
            "response-required": False,
            "correlation-id": dittoCorrelationId
        }
    def prepareSupResponse(self,agent,rolloutCorrelationId,status,message,swModule = None):
        self.headers = {
            "response-required": False,
            "content-type": "application/json"
        }
        self.value = {}
        self.value["definition"] =  [
                "org.eclipse.hawkbit.swupdatable:SoftwareUpdatable:2.0.0"
        ]
        self.value["properties"] = {}
        self.value["properties"]["status"] = {
            "agentName": agent.name,
            "agentVersion": agent.version,
            "softwareModuleType": agent.type
        }
        self.value["properties"]["status"]["lastOperation"] = {
                       "status": status,
                        "message": message,
                        "correlationId": rolloutCorrelationId,
                        "softwareModule": {
                            "name": "sw2",
                            "version": "1"
                        }
        }

        if swModule:
            self.value["properties"]["status"]["lastOperation"]["softwareModule"] = {
                "name": swModule.name,
                "version": swModule.version
            }
        
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)