# Queue Processing Revisited

In this section we re-visit the Queue processing Azure Function and integrate CosmoDB

## Code

Update the [functions/queue-processor/ServiceBusQueueTrigger/__init__.py](../functions/queue-processor/ServiceBusQueueTrigger/__init__.py) file with the following code

```python
import azure.functions as func
import azure.cosmos.cosmos_client as cosmos_client
import logging
import json
import uuid

config = {
    'ENDPOINT': 'https://trashe.documents.azure.com',
    'PRIMARYKEY': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'DATABASE': 'TrasheList',
    'CONTAINER': 'Items'
}

# Initialize the Cosmos client
client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={
                                    'masterKey': config['PRIMARYKEY']})

# Get reference to DB
database_link = 'dbs/' + config['DATABASE']
db = client.ReadDatabase(database_link)

# Get reference tocontainer
container_link = database_link + '/colls/{0}'.format(config['CONTAINER'])
container = client.ReadContainer(container_link)

def main(msg: func.ServiceBusMessage):
    result = msg.get_body().decode('utf-8')
    results = json.loads(result)
    item_payload = {
        'id': str(uuid.uuid1()),
        'timestamp': results['created'],
        'prediction': results['predictions']['tagName'],
        'probability': results['predictions']['probability']
    }
    # Only post if higher then 50%
    if results['predictions']['probability'] > 0.5:
        # Create and add some items to the container
        item = client.CreateItem(container['_self'], item_payload)
```

You can get the `'PRIMARYKEY'` variable from the Connection String query under `Primary SQL Connection String`

```bash
# Get the connection string for API account
az cosmosdb list-connection-strings \
    --name "trashe" \
    --resource-group "azure-iot-trashe"
```

## Deploy

```bash
cd functions/queue-processor
func azure functionapp publish trashe-queue-processor --build-native-deps
```
