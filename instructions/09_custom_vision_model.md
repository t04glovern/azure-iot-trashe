# Custom Vision Model Creation

## Custom Vision Deploy

```bash
cd templates/custom-vision
./deploy.sh

# Your subscription ID can be looked up with the CLI using: az account show --out json
# Enter your subscription ID:
XXXXXXX-XXXXXXXXXX-XXXXXXXXXXXX-XXXXXXXXXX

# Enter a resource group name
azure-iot-trashe

# Enter a name for this deployment:
azure-iot-trashe-vision

# You can lookup locations with the CLI using: az account list-locations
# Enter resource group location:
australiasoutheast
```

## Custom Vision Train

Navigate to the [https://www.customvision.ai/projects](https://www.customvision.ai/projects) page.

Create a new project and model selecting the following settings

![Custom Vision Setup 1](img/custom-vision-create-01.png)

Make use of [Trashnet](https://github.com/garythung/trashnet) to build a trash dataset

```bash
wget https://github.com/garythung/trashnet/raw/master/data/dataset-resized.zip
unzip dataset-resized.zip
```

![Custom Vision Setup 2](img/custom-vision-create-02.png)

![Custom Vision Setup 3](img/custom-vision-create-03.png)

Export the model along with the Dockerfile. Replace the `labels.txt` and `model.pb` in `modules/image-classifier/app`

![Custom Vision Setup 4](img/custom-vision-create-04.png)

## Delete

To delete the deployment, run the following

```bash
az group deployment delete \
    --name "azure-iot-trashe-vision" \
    --resource-group "azure-iot-trashe"
```
