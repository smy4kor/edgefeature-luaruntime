import json

class DittoResponse:
    def __init__(self,topic,path,responseCode):
        self.topic = topic
        self.path = path
        self.value = {} ## let the caller decide what it wants to send
        self.headers = {}
        self.status = responseCode
    def appendSubscriptionInfo(self,subscriptionInfo):
        self.value["thingId"] = subscriptionInfo.deviceId
        self.value["policyId"] = subscriptionInfo.policyId
        self.headers["reply-to"] = "command/" + subscriptionInfo.hubTenantId
    def noResponse(self):
        self.headers["response-required"] = False
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)