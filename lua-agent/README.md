# Lua Agent
This is a groovy based implementation which does the following:
- Register a [software updatable](https://vorto.eclipseprojects.io/#/details/org.eclipse.hawkbit.swupdatable:SoftwareUpdatable:2.0.0) agent of type "lua".
- Subscribe for download or install operation commands using the [mqtt announcements](https://docs.bosch-iot-suite.com/edge/index.html#109654.htm).

- The Edge agent runs a [local mosquitto](https://docs.bosch-iot-suite.com/edge/index.html#109654.htm) to enable communication with Iot-Things. See the [Complete ditto protocol here](https://www.eclipse.org/ditto/1.5/protocol-specification-things-create-or-modify.html)
    - [Another reference](https://wiki.bosch-si.com/display/MBSIOTSDK/Things+Protocol+Patterns#ThingsProtocolPatterns-Command.1)

# How to run
- Copy the python-scripts to the configured\provisioned mBS device.
- Run `python subscribe-for-commands.py`.
- If python is not installed, install it manually as done in the dockerfile.

## Sample Console Outputs

* For a install command

```
MQTT topic: command///req/01fp-pdid6m-12i8u431qmpi1b-1xalkwfreplies/install
Ditto topic: com.peter2/aa-machine-1/things/live/messages/install
Ditto originator: iot-suite:S-1-5-21-1937855695-3964793637-879644401-803447/service-instance.55cc1e7a-f2b7-4e3e-9193-d69f11564ede.iot-things@device-management
Service instance id: 55cc1e7a-f2b7-4e3e-9193-d69f11564ede
Path: /features/manually-created-lua-agent/inbox/messages/install
Is install command: True
Is software updatable command: True
request id is: 01fp-pdid6m-12i8u431qmpi1b-1xalkwfreplies
```

* For an attribute change

```
MQTT topic: command///req//created
Ditto topic: com.peter2/aa-machine-1/things/twin/events/created
Ditto originator: iot-suite:S-1-5-21-1937855695-3964793637-879644401-803447/service-instance.55cc1e7a-f2b7-4e3e-9193-d69f11564ede.iot-things@device-management
Service instance id: 55cc1e7a-f2b7-4e3e-9193-d69f11564ede
Path: /attributes/rollouts/assignedDS/168602/date
Is install command: False
Is software updatable command: False

```

# Other Examples
This section has some examples to help you become familiar with some of the technologies used in this demo.

## Mosquitto
 So if you wish to have a local setup of mosquitto then:
- install mosquitto locally using ```sudo apt-get install mosquitto```.
- Run `python3 examples/mosquitto-connection-test.py``` to check if you receive a message after executing the next step.
- Publish a message ```mosquitto_pub -m "message from mosquitto_pub client" -t "test"``` locally.
- [check out this document for more](https://www.vultr.com/docs/how-to-install-mosquitto-mqtt-broker-server-on-ubuntu-16-04).