#!/usr/bin/python3

import time
import json
import os, sys

import urllib.request

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir + "/python-scripts")
print(parentdir)

from commands import DittoCommand
from dittoresponse import DittoResponse
from executor import ScriptExecutor

#====== end of imports ================

def downloadFile(art):
    path = os.getcwd() + "/downloads"
    print ("Desired download directory is %s" % path)
    if  not os.path.isdir(path):
        print("Download directory must be created")
        try:
            os.mkdir(path)
            print ("Successfully created the directory %s " % path)
        except OSError:
            print ("Creation of the directory %s failed" % path)

    urllib.request.urlretrieve(art.url, path + "/" + art.name)
    print('downloaded ' + art.name)

def simulateResponse():
    rsp = DittoResponse("com.bosch.edge/demo/things/twin/commands/modify","path1",200)
    print(rsp.toJson())
    
jsonStrInput = "{\"topic\":\"com.peter2/aa-machine-1/things/live/messages/install\",\"headers\":{\"version\":2,\"ditto-originator\":\"iot-suite:S-1-5-21-1937855695-3964793637-879644401-803447/service-instance.55cc1e7a-f2b7-4e3e-9193-d69f11564ede.iot-things@device-management\",\"requested-acks\":[],\"response-required\":true,\"correlation-id\":\"p-pdid6m-12i8u431qmpi1b-1l4lsr4\",\"content-type\":\"application/json\",\"x-things-parameter-order\":\"[\\\"update\\\"]\"},\"path\":\"/features/manually-created-lua-agent/inbox/messages/install\",\"value\":{\"metaData\":{},\"softwareModules\":[{\"metaData\":{},\"softwareModule\":{\"name\":\"concat\",\"version\":\"1\"},\"artifacts\":[{\"checksums\":{\"SHA256\":\"c23b1efcfa208c43e4d9f62572483132f90430726f2694bc8ab0d9f1ef3c57c6\",\"SHA1\":\"c3513628d801d3f29c0fa6a8b86962d1e3e73b36\",\"MD5\":\"036ea6cdb3ce8aca6a79dab0ad22a944\"},\"download\":{\"HTTPS\":{\"md5url\":\"https://cdn.eu1.bosch-iot-rollouts.com/AFD0315A-B66F-4E17-B8B0-A8AE7D66E5F4/c3513628d801d3f29c0fa6a8b86962d1e3e73b36?Expires=1616078455&Signature=QNRFDUuEM4o4MEqxV-QOjPlvIQTBl67HwRKVld8edpfAU~IpAA0kvO~N2fexj~Gn9~zAPrvRyIWEW9tuVbHvHS9zwKmqVsucR77RSCRHa-2kMptuPAgGU0-GiexZmqVNdX0BZhMAb0BXM-SZxS0vnRQzjPtE46Dxfd21LrQAyMkGjWZ8YoRQJJp2GHu47i4h83M0XIipw2tpW8b5OYzNoXdwPQvykR8Aq90xMhAUKbHl4aViSyseWTRxLZvS0uq0tRd5Sw1vf3R7qvRzCfWkzw3uPebD8UuoyZ1dlM58ePd3q5PiS1dRAVWrKoZUu~4sATsXWgD~rlhWQ64B311ARQ__&Key-Pair-Id=APKAJ7V55VK3Y2WFZOHQ\",\"url\":\"https://cdn.eu1.bosch-iot-rollouts.com/AFD0315A-B66F-4E17-B8B0-A8AE7D66E5F4/c3513628d801d3f29c0fa6a8b86962d1e3e73b36?Expires=1616078455&Signature=QNRFDUuEM4o4MEqxV-QOjPlvIQTBl67HwRKVld8edpfAU~IpAA0kvO~N2fexj~Gn9~zAPrvRyIWEW9tuVbHvHS9zwKmqVsucR77RSCRHa-2kMptuPAgGU0-GiexZmqVNdX0BZhMAb0BXM-SZxS0vnRQzjPtE46Dxfd21LrQAyMkGjWZ8YoRQJJp2GHu47i4h83M0XIipw2tpW8b5OYzNoXdwPQvykR8Aq90xMhAUKbHl4aViSyseWTRxLZvS0uq0tRd5Sw1vf3R7qvRzCfWkzw3uPebD8UuoyZ1dlM58ePd3q5PiS1dRAVWrKoZUu~4sATsXWgD~rlhWQ64B311ARQ__&Key-Pair-Id=APKAJ7V55VK3Y2WFZOHQ\"}},\"filename\":\"concat.lua\",\"size\":96}]},{\"metaData\":{},\"softwareModule\":{\"name\":\"add\",\"version\":\"1\"},\"artifacts\":[{\"checksums\":{\"SHA256\":\"7b6917667578826dfb3e80c23756f5130cc6ac8deed5ad419cec797afc12f5dd\",\"SHA1\":\"1f03725200eb07b0bd88c24e42e973d6f06424af\",\"MD5\":\"2e2c24169b9fceb5cfd3eea8af0d3581\"},\"download\":{\"HTTPS\":{\"md5url\":\"https://cdn.eu1.bosch-iot-rollouts.com/AFD0315A-B66F-4E17-B8B0-A8AE7D66E5F4/1f03725200eb07b0bd88c24e42e973d6f06424af?Expires=1616078455&Signature=EIZIiZ4vDUiccQ8tQegFbyPImzln3bzuYutaV-SnXVhCO~1J1dxyJwpFRBCNwajkyebTQJuwIz1wck~7bN4JtltYyZ5GrytJfzU1Hzod7tt2NNXEJY6Q3vQAC5zDkZ6aIQ0LRpS~2JEs3ohGQ5rJYM6T1-7h61J2xZLappsVqnsObMwOnmUf9TR9eTfMDXC-ABdC-AUdLn9vad1NkYRo-42flUFqIgKqFYQdftxb-kfQpBcAm73npIPHx~O1m04dasyh3T9c2EhJ1bjbOBH4mRAyXlUVy9G8Kg4sFmt5Rwh79Lvob8HHX4If4sDuGv85zd79lalwtg6UX44qvByikQ__&Key-Pair-Id=APKAJ7V55VK3Y2WFZOHQ\",\"url\":\"https://cdn.eu1.bosch-iot-rollouts.com/AFD0315A-B66F-4E17-B8B0-A8AE7D66E5F4/1f03725200eb07b0bd88c24e42e973d6f06424af?Expires=1616078455&Signature=EIZIiZ4vDUiccQ8tQegFbyPImzln3bzuYutaV-SnXVhCO~1J1dxyJwpFRBCNwajkyebTQJuwIz1wck~7bN4JtltYyZ5GrytJfzU1Hzod7tt2NNXEJY6Q3vQAC5zDkZ6aIQ0LRpS~2JEs3ohGQ5rJYM6T1-7h61J2xZLappsVqnsObMwOnmUf9TR9eTfMDXC-ABdC-AUdLn9vad1NkYRo-42flUFqIgKqFYQdftxb-kfQpBcAm73npIPHx~O1m04dasyh3T9c2EhJ1bjbOBH4mRAyXlUVy9G8Kg4sFmt5Rwh79Lvob8HHX4If4sDuGv85zd79lalwtg6UX44qvByikQ__&Key-Pair-Id=APKAJ7V55VK3Y2WFZOHQ\"}},\"filename\":\"add.lua\",\"size\":39}]}],\"forced\":true,\"weight\":\"None\",\"correlationId\":\"f706a5ca-60d1-4fa5-9685-d454faef772f\"}}"

topicFromMqttMessage = "command///req/01fp-pdid6m-12i8u431qmpi1b-1m2zqv2replies/install"  
cmd = DittoCommand(json.loads(jsonStrInput),topicFromMqttMessage)
cmd.printInfo();
print("Rollouts correlationId is: " + str(cmd.getRolloutsCorrelationId()))

for swMod in cmd.getSoftwareModules():
    for art in swMod.artifacts:
        downloadFile(art)
simulateResponse()


#    print(swMod.toJson())


