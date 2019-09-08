# Azure IoT

## Azure CLI Setup

```bash
pip install --upgrade azure-cli

# NOT REQUIRED if you dont need local testing (likely to not work)
# https://github.com/Azure/iotedgehubdev#installing
sudo su
pip3 install --upgrade iotedgehubdev
iotedgehubdev setup -c "<connection-string>"
```

Login to the CLI

```bash
az login
```

### Install the IoT Extension

```bash
az extension add --name azure-cli-iot-ext
```

## IoT Hub Deploy

**NOTE**: Some values used are hardcoded into `templates/azure-iot-hub/parameters.json`. At a minimum you should be modifying `name` to change the name of your IOT hub as this name needs to be unique.
You can also use azure IOT Hub command `az iot hub create --name $hubName --resource-group {Your resource group name} --sku "S1" --location {Azure location}`


```bash
cd templates/azure-iot-hub
./deploy.sh

# Your subscription ID can be looked up with the CLI using: az account show --query id
# Enter your subscription ID:
XXXXXXX-XXXXXXXXXX-XXXXXXXXXXXX-XXXXXXXXXX

# Enter a resource group name
azure-iot-trashe

# Enter a name for this deployment:
azure-iot-trashe-iot-hub

# You can lookup locations with the CLI using: az account list-locations
# Enter resource group location:
australiasoutheast
```

## IoT Device Create

```bash
az iot hub device-identity create \
  --device-id "trashe-rpi-01" \
  --hub-name "azure-iot-trashe-hub" \
  --edge-enabled
```

Get the connection string

```bash
az iot hub device-identity show-connection-string \
  --device-id "trashe-rpi-01" \
  --hub-name "azure-iot-trashe-hub"
```

## Raspberry Pi Connection Daemon

Open the following file (or create the file if it doesnt exist)

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

If you're doing this for multiple devices, you could consider using the [IOT Device Provisioning Service](https://docs.microsoft.com/en-us/azure/iot-dps/quick-setup-auto-provision-cli)

Restart the edgeiot service

```bash
sudo systemctl restart iotedge
systemctl status iotedge
```

List the Modules running on the device

```bash
sudo iotedge list
```

## Delete

To delete the deployment, run the following

```bash
az group deployment delete \
  --name "azure-iot-trashe-iot-hub" \
  --resource-group "azure-iot-trashe"
```
