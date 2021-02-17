import json

class SubscriptionInfo:
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    def compute(self,payload):
        # See https://docs.bosch-iot-suite.com/edge/index.html#109655.htm
        self.deviceId = payload["deviceId"]
        self.hubTenantId = payload["tenantId"]
        self.policyId = payload["policyId"]
        print("Device information is \n" + self.toJson())
