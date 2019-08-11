# Service Bus Setup

## Create Service Bus

```bash
export subscriptionID=$(az account show --query id -o tsv)

# Create a Service Bus messaging namespace with a unique name
az servicebus namespace create \
    --resource-group "azure-iot-trashe" \
    --name "trashe" \
    --location australiasoutheast

# Create a Service Bus queue
az servicebus queue create \
    --resource-group "azure-iot-trashe" \
    --namespace-name "trashe" \
    --name "trashe-process"

# Create the authorization rule for the Service Bus queue.
az servicebus queue authorization-rule create \
    --name "sbauthrule" \
    --namespace-name "trashe" \
    --queue-name "trashe-process" \
    --resource-group "azure-iot-trashe" \
    --rights Listen Manage Send \
    --subscription $subscriptionID
```

## IoT Routing

```bash
# Get the Service Bus queue connection string.
# The "-o tsv" ensures it is returned without the default double-quotes.
export sbqConnectionString=$(az servicebus queue authorization-rule keys list \
    --name "sbauthrule" \
    --namespace-name "trashe" \
    --queue-name "trashe-process" \
    --resource-group "azure-iot-trashe" \
    --subscription $subscriptionID \
    --query primaryConnectionString -o tsv)

# Set up the routing endpoint for the Service Bus queue.
# This uses the Service Bus queue connection string.
az iot hub routing-endpoint create \
    --connection-string $sbqConnectionString \
    --endpoint-name "azure-iot-trashe-service-bus" \
    --endpoint-resource-group "azure-iot-trashe" \
    --endpoint-subscription-id $subscriptionID \
    --endpoint-type "ServiceBusQueue" \
    --hub-name "azure-iot-trashe-hub" \
    --resource-group "azure-iot-trashe"

# Set up the message route for the Service Bus queue endpoint.
az iot hub route create --name "azure-iot-trashe-cam-route" \
    --hub-name "azure-iot-trashe-hub" \
    --source-type devicemessages \
    --resource-group "azure-iot-trashe" \
    --endpoint-name "azure-iot-trashe-service-bus" \
    --enabled \
    --condition "true"
```
