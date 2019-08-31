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
    # {
    #     "id": "",
    #     "predictions": {
    #         "probability": 0.2551375,
    #         "boundingBox": {
    #             "left": 0.00870211,
    #             "height": 0.82958604,
    #             "top": 0.01420201,
    #             "width": 0.53497158
    #         },
    #         "tagId": 5,
    #         "tagName": "glass container"
    #     },
    #     "created": "2019-08-31T12:25:58.163379",
    #     "project": "",
    #     "iteration": ""
    # }

    # Only post if higher then 50%
    if results['predictions']['probability'] > 0.5:
        # Create and add some items to the container
        item = client.CreateItem(container['_self'], item_payload)
