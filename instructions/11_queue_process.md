# Queue Processor

## Deploy Function

Install the [Core tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local#v2)

```bash
npm install -g azure-functions-core-tools
```

### Setup Python

```bash
# Bash
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
source .venv/Scripts/activate
pip install azure
```

### Create the function

```bash
func init queue-processor
cd queue-processor
func new
```

### Update Variables

Open [functions/queue-processor/ServiceBusQueueTrigger/function.json](../functions/queue-processor/ServiceBusQueueTrigger/function.json) and update the settings with your queue details.

```json
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "name": "msg",
      "type": "serviceBusTrigger",
      "direction": "in",
      "queueName": "trashe-process",
      "connection": "AzureServiceBusConnectionString"
    }
  ]
}
```

You can get the connection string using the following:

```bash
az servicebus namespace authorization-rule keys list \
    --resource-group "azure-iot-trashe" \
    --namespace-name "trashe" \
    --name RootManageSharedAccessKey \
    --query primaryConnectionString \
    --output tsv
```

Editthe file called `local.settings.json` with the following settings

```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "{AzureWebJobsStorage}"
  },
  "ConnectionStrings": {
    "AzureServiceBusConnectionString": "Endpoint=sb://trashe.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  }
}
```

### Create Storage account

```bash
az storage account create \
    --name "trashe" \
    --location australiasoutheast \
    --resource-group "azure-iot-trashe" \
    --sku Standard_LRS
```

### Create Function App

```bash
az functionapp create \
    --resource-group "azure-iot-trashe" \
    --os-type Linux \
    --consumption-plan-location westeurope \
    --runtime python \
    --name "trashe-queue-processor" \
    --storage-account "trashe"
```

Create a new connection string for the app

```bash
az webapp config connection-string set \
    --resource-group "azure-iot-trashe" \
    --name "trashe-queue-processor" \
    --connection-string-type custom \
    --settings AzureServiceBusConnectionString="Endpoint=sb://trashe.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

### Deploy the App

```bash
func azure functionapp publish trashe-queue-processor --build-native-deps
```

## Attribution

* [Create an HTTP triggered function in Azure](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python)
