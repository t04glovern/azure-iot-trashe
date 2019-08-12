#To make python 2 and python 3 compatible code
from __future__ import absolute_import

#Returns rectangle boundaries in the CV2 format (topLeftX, topLeftY, bottomRightX, bottomRightY) given by a processing service
class AnnotationParser:
    def getCV2RectanglesFromProcessingService1(self, response):
        # {
        #     "id": "",
        #     "iteration": "",
        #     "created": "2019-08-12T13:16:54.061026",
        #     "project": "",
        #     "predictions": {
        #         "probability": 0.16118199,
        #         "tagId": 5,
        #         "tagName": "glass container",
        #         "boundingBox": {
        #             "left": 0.09786242,
        #             "height": 0.67044513,
        #             "width": 0.65364401,
        #             "top": 0.31096364
        #         }
        #     }
        # }
        try:
            listOfCV2Rectangles = []
            top = response["predictions"]['boundingBox']['top']
            left = response["predictions"]['boundingBox']['left']
            width = response["predictions"]['boundingBox']['width']
            height = response["predictions"]['boundingBox']['height']
            if top is not None and left is not None and width is not None and height is not None:
                topLeftX = left
                topLeftY = top
                bottomRightX = left + width
                bottomRightY = top + height
                listOfCV2Rectangles.append([topLeftX, topLeftY, bottomRightX, bottomRightY])
            return listOfCV2Rectangles
        except:
            #Ignoring exceptions for now so that video can be read and analyzed without post-processing in case of errors
            pass