# edgefeature-luaruntime
Containerized LUA runtime, acting as a SoftwareUpdatable-feature for the Bosch IoT Suite

# How to run without dockerfile
- Download the edge agent. Copy the device `provisioning.json` to the directory containing the `start.sh`. See [how to register a device](https://docs.bosch-iot-suite.com/device-management/Register-a-device-via-the-Bosch-IoT-Manager-UI.html) if this step is not familiar.
- Manually create a [software updatable](https://vorto.eclipseprojects.io/#/details/org.eclipse.hawkbit.swupdatable:SoftwareUpdatable:2.0.0) lua feature in iot-things as shown below. This step will be automated soon.

```json
    "feature-id-here": {
            "definition": [
                "org.eclipse.hawkbit.swupdatable:SoftwareUpdatable:2.0.0"
            ],
            "properties": {
                "status": {
                    "agentName": "lua",
                    "agentVersion": "2.0.0",
                    "softwareModuleType": "lua"
                }
            }
        }
```
- Install the following prerequisites if you are not using the docker image.

```
yum -y install python3
alias python=python3
sudo apt install python3-pip
pip3 install paho-mqtt python-etcd
pip3 install lupa
```
- Run `python python-scripts/start-lua-agent.py`.
- Open rollouts and assign a distributionSet to this device.

# How to run using docker image
This approach is not tested 
* Modify the code to use `ctrhost` as mosquitto host. Ex: ```client.connect("ctrhost", 1883)```
* Build the dockerfile and push the image to a repository which is publically available.
* Please see [how to deploy a container](https://docs.bosch-iot-suite.com/edge/index.html#109664.htm). It describes how to remotely trigger installation of containers on gateways in the form of Software Updates from Bosch IoT Suite Rollouts service.
* In the above step, make sure that you configure `extra_hosts` as shown below.

```
{
   "container_name": "your-container-name",
   "image": {
      "name": "image-ref"
   },
   "host_config": {
      "extra_hosts": [
         "ctrhost:host_ip"
      ]
   }
}
```

# References
* [Registering a device](https://docs.bosch-iot-suite.com/device-management/Register-a-device-via-the-Bosch-IoT-Manager-UI.html).
* [Ditto protocol](https://www.eclipse.org/ditto/1.5/protocol-specification-things-create-or-modify.html)
* [Software updatable integration suite](https://docs.bosch-iot-suite.com/device-management/SoftwareUpdatable-feature-detailed-specification-and-integration-guide.html).

