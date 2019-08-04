# Azure IoT

## Azure CLI Setup

```bash
# MacOS
brew update && brew install azure-cli

# Python Pip
pip install azure-cli
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

**NOTE**: Some values used are hardcoded into `templates/azure-iot-hub/parameters.json`. Make sure to edit it before deploying if you are doing this in production

```bash
cd templates/azure-iot-hub
./deploy.sh

# Your subscription ID can be looked up with the CLI using: az account show --out json
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
