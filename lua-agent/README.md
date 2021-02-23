# How to run
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
- Install the following prerequisites.

```
yum -y install python3
alias python=python3
sudo apt install python3-pip
pip3 install paho-mqtt python-etcd
pip3 install lupa
```
- Run `python python-scripts/subscribe-for-commands.py`.
- Open rollouts and assign a distributionSet to this device.

# References
* [Registering a device](https://docs.bosch-iot-suite.com/device-management/Register-a-device-via-the-Bosch-IoT-Manager-UI.html).
* [Ditto protocol](https://www.eclipse.org/ditto/1.5/protocol-specification-things-create-or-modify.html)
* [Software updatable integration suite](https://docs.bosch-iot-suite.com/device-management/SoftwareUpdatable-feature-detailed-specification-and-integration-guide.html).
