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
    def prepareSupResponse(self,rolloutCorrelationId,status,message,swModule = None):
        self.headers = {
            "response-required": False,
            "content-type": "application/json"
        }
        self.value = {
            "status": status,
            "message": message,
            "correlationId": rolloutCorrelationId
        }
        if swModule:
            self.value["softwareModule"] = {
                "name": swModule.name,
                "version": swModule.version
            }
        
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)