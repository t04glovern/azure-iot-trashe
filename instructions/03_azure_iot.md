# Azure IoT

## Azure CLI Setup

```bash
brew update && brew install azure-cli
```

Login to the CLI

```bash
az login
```

## IoT Hub Deploy

```bash
cd templates/azure-iot-hub
./deploy.sh

# Your subscription ID can be looked up with the CLI using: az account show --out json
# Enter your subscription ID:
XXXXXXX-XXXXXXXXXX-XXXXXXXXXXXX-XXXXXXXXXX
# This script will look for an existing resource group, otherwise a new one will be created
# You can create new resource groups with the CLI using: az group create
# Enter a resource group name
azure-iot-powermon
# Enter a name for this deployment:
azure-iot-powermon-iot-hub
# If creating a *new* resource group, you need to set a location
# You can lookup locations with the CLI using: az account list-locations
# Enter resource group location:
australiasoutheast
```

## IoT Device Create

```bash
az iot hub device-identity create \
    --device-id "powermon-rpi-01" \
    --hub-name "azure-iot-powermon-hub" \
    --edge-enabled
# {
#   "authentication": {
#     "symmetricKey": {
#       "primaryKey": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#       "secondaryKey": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
#     },
#     "type": "sas",
#     "x509Thumbprint": {
#       "primaryThumbprint": null,
#       "secondaryThumbprint": null
#     }
#   },
#   "capabilities": {
#     "iotEdge": true
#   },
#   "cloudToDeviceMessageCount": 0,
#   "connectionState": "Disconnected",
#   "connectionStateUpdatedTime": "0001-01-01T00:00:00",
#   "deviceId": "powermon-rpi-01",
#   "deviceScope": "ms-azure-iot-edge://powermon-rpi-01-637002575398722524",
#   "etag": "NDA5OTUzNzQ3",
#   "generationId": "637002575398722524",
#   "lastActivityTime": "0001-01-01T00:00:00",
#   "status": "enabled",
#   "statusReason": null,
#   "statusUpdatedTime": "0001-01-01T00:00:00"
# }
```

Get the connection string

```bash
az iot hub device-identity show-connection-string \
    --device-id "powermon-rpi-01" \
    --hub-name "azure-iot-powermon-hub"
# {
#   "connectionString": "HostName=azure-iot-powermon-hub.azure-devices.net;DeviceId=powermon-rpi-01;SharedAccessKey=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# }
```

## Raspberry Pi Connection Daemon

Open the following file (or create it if it doesnt exist)

```bash
sudo nano /etc/iotedge/config.yaml
```

Update the `device_connection_string` with the connection string from above

```yaml
# Manual provisioning configuration
provisioning:
  source: "manual"
  device_connection_string: "<ADD DEVICE CONNECTION STRING HERE>"
```

Restart the edgeiot service

```bash
systemctl status iotedge
# ● iotedge.service - Azure IoT Edge daemon
#    Loaded: loaded (/lib/systemd/system/iotedge.service; enabled; vendor preset: enabled)
#    Active: active (running) since Thu 2019-08-01 14:02:40 BST; 6s ago
#      Docs: man:iotedged(8)
#  Main PID: 18638 (iotedged)
#     Tasks: 10 (limit: 2200)
#    Memory: 9.9M
#    CGroup: /system.slice/iotedge.service
#            └─18638 /usr/bin/iotedged -c /etc/iotedge/config.yaml

# Aug 01 14:02:40 raspberrypi iotedged[18638]: 2019-08-01T13:02:40Z [INFO] - Using runtime network id azure-iot-edge
# Aug 01 14:02:40 raspberrypi iotedged[18638]: 2019-08-01T13:02:40Z [INFO] - Initializing the module runtime...
# Aug 01 14:02:40 raspberrypi iotedged[18638]: 2019-08-01T13:02:40Z [INFO] - Initializing module runtime...
# Aug 01 14:02:41 raspberrypi iotedged[18638]: 2019-08-01T13:02:41Z [INFO] - Successfully initialized module runtime
# Aug 01 14:02:41 raspberrypi iotedged[18638]: 2019-08-01T13:02:41Z [INFO] - Finished initializing the module runtime.
# Aug 01 14:02:41 raspberrypi iotedged[18638]: 2019-08-01T13:02:41Z [INFO] - Configuring /var/lib/iotedge as the home directory.
# Aug 01 14:02:41 raspberrypi iotedged[18638]: 2019-08-01T13:02:41Z [INFO] - Configuring certificates...
# Aug 01 14:02:41 raspberrypi iotedged[18638]: 2019-08-01T13:02:41Z [INFO] - Transparent gateway certificates not found, operating in quick start mode...
# Aug 01 14:02:41 raspberrypi iotedged[18638]: 2019-08-01T13:02:41Z [INFO] - Finished configuring certificates.
# Aug 01 14:02:41 raspberrypi iotedged[18638]: 2019-08-01T13:02:41Z [INFO] - Initializing hsm...
# ...
# Aug 01 14:07:03 raspberrypi iotedged[18638]: 2019-08-01T13:07:03Z [INFO] - Checking edge runtime status
# Aug 01 14:07:03 raspberrypi iotedged[18638]: 2019-08-01T13:07:03Z [INFO] - Edge runtime is running.
# Aug 01 14:07:03 raspberrypi iotedged[18638]: 2019-08-01T13:07:03Z [INFO] - Checking edge runtime status
# Aug 01 14:07:03 raspberrypi iotedged[18638]: 2019-08-01T13:07:03Z [INFO] - Edge runtime is running.
# Aug 01 14:07:20 raspberrypi iotedged[18638]: 2019-08-01T13:07:20Z [INFO] - Querying system info...
# Aug 01 14:07:20 raspberrypi iotedged[18638]: 2019-08-01T13:07:20Z [INFO] - Successfully queried system info
```

List the Modules running on the device

```bash
sudo iotedge list
```
