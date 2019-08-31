import azure.functions as func
import azure.cosmos.cosmos_client as cosmos_client
import logging
import json

config = {
    'ENDPOINT': 'https://trashe.documents.azure.com',
    'PRIMARYKEY': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'DATABASE': 'TrasheList',
    'CONTAINER': 'Items'
}

# Initialize the Cosmos client
client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={
                                    'masterKey': config['PRIMARYKEY']})


def main(msg: func.ServiceBusMessage):
    result = msg.get_body().decode('utf-8')
    logging.info(result)
    # {
    #     "project": "",
    #     "created": "2019-08-11T13:11:59.609447",
    #     "predictions": {
    #         "probability": 0.9841981530189514,
    #         "tagName": "paper",
    #         "boundingBox": null,
    #         "tagId": ""
    #     },
    #     "iteration": "",
    #     "id": ""
    # }

    # Create and add some items to the container
    item = client.CreateItem(config['CONTAINER'], result)
