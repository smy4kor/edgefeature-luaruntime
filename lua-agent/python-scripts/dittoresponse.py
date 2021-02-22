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
    def prepareSupResponse(self,cmd,status,message):
        self.headers = {
            "response-required": False
        }
        self.value = {
                        "status": status,
                        "message": message,
                        "correlationId": "98d52822-9dff-4126-a65d-d4c2f4d8d373",
                        "softwareModule": {
                            "name": "sw2",
                            "version": "1"
                }
        }
        
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)