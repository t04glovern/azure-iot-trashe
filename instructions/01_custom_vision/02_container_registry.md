# Container Registry Create
Create a custom docker repository (Azure Container Manager) to securely hold your docker image and make it available via Azure. You can do this in two ways
1. ```az acr create --resource-group YOUR_RESOURCE_GROUP_NAME --name YOUR_REPOSITORY_NAME --sku "Standard"```
2. Through the Azure Resource Manager (ARM) template in templates/container-registry. You will need to change ```registryName ``` and ```registryLocation``` in ```parameters.json```

```bash
cd templates/container-registry
./deploy.sh

# Your subscription ID can be looked up with the CLI using: az account show --query id
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

This created a container registry to allow you to store your docker image securely within Azure.

Login to your docker registry with the name that you used. You can see more Azure Container Registry commands [here](https://docs.microsoft.com/en-us/cli/azure/acr?view=azure-cli-latest).

```bash
az acr login --name "glover"
```

Upload the image classifier that you created in step 1, ```modules/image-classifier/``` into your docker registry, replacing ```glover``` with the name of the registry you created.
You should also change `````` in ```modules/image-classifier/module.json``` to the name of your container registry.
```docker build  --rm -f ./modules/image-classifier/Dockerfile.arm32v7 -t glover.azurecr.io/image-classifier:0.0.1-arm32v7 ./modules/image-classifier && docker push glover.azurecr.io/image-classifier:0.0.1-arm32v7
```

You can list docker images in your docker repository with ```az acr repository list -n  {The name of your repository}```.

## Delete

To delete the deployment, run the following

```bash
az group deployment delete \
    --name "azure-iot-trashe-registry" \
    --resource-group "azure-iot-trashe"
```