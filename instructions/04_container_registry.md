# Container Registry Create

**NOTE**: The name of the registry used is hardcoded into `templates/container-registry/parameters.json`. Make sure to edit it before deploying if you are doing this in production

```bash
cd templates/container-registry
./deploy.sh

# Your subscription ID can be looked up with the CLI using: az account show --out json
# Enter your subscription ID:
XXXXXXX-XXXXXXXXXX-XXXXXXXXXXXX-XXXXXXXXXX

# Enter a resource group name
azure-iot-trashe

# Enter a name for this deployment:
azure-iot-trashe-registry

# You can lookup locations with the CLI using: az account list-locations
# Enter resource group location:
australiasoutheast
```

This created a container registry for me called `glover`

Login to docker

```bash
az acr login --name "glover"
```

## Delete

To delete the deployment, run the following

```bash
az group deployment delete \
    --name "azure-iot-trashe-registry" \
    --resource-group "azure-iot-trashe"
```
