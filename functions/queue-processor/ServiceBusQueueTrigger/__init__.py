import azure.functions as func

import logging
import json

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
