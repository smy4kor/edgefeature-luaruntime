
class DittoResponse:
    def __init__(self,topic,path):
        self.topic = topic
        self.path = path
        self.value = {} ## let the caller decide what it wants to send
        self.headers = {}