# Lua Agent
This is a groovy based implementation which does the following:
- Register a [software updatable](https://vorto.eclipseprojects.io/#/details/org.eclipse.hawkbit.swupdatable:SoftwareUpdatable:2.0.0) agent of type "lua".
- Subscribe for download or install operation commands using the [mqtt announcements](https://docs.bosch-iot-suite.com/edge/index.html#109654.htm).


# Developer Examples
This section has some examples to help you become familiar with some of the technologies used in this demo.

## Mosquitto
The Edge agent runs a [local mosquitto](https://docs.bosch-iot-suite.com/edge/index.html#109654.htm) to enable communication with Iot-Things. So if you wish to have a local setup of mosquitto then:
- install mosquitto locally using ```sudo apt-get install mosquitto```.
- Run `python3 examples/mosquitto-connection-test.py``` to check if you receive a message after executing the next step.
- Publish a message ```mosquitto_pub -m "message from mosquitto_pub client" -t "test"``` locally.
- [check out this document for more](https://www.vultr.com/docs/how-to-install-mosquitto-mqtt-broker-server-on-ubuntu-16-04).