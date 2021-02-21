import json

class DittoResponse:
    def __init__(self,topic,path,responseCode):
        self.topic = topic
        self.path = path
        self.status = responseCode
    def prepareAknowledgement(self,subscriptionInfo):
        self.value = {
            "thingId": subscriptionInfo.deviceId,
            "policyId": subscriptionInfo.policyId
        }
        self.headers = {
            "response-required": False,
            "reply-to": "command/" + subscriptionInfo.hubTenantId
        }
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)