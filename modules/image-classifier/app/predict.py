import sys
import tensorflow as tf
import numpy as np
from PIL import Image
from urllib.request import urlopen
from datetime import datetime
from object_detection import ObjectDetection

MODEL_FILENAME = 'model.pb'
LABELS_FILENAME = 'labels.txt'

od_model = None

class TFObjectDetection(ObjectDetection):
    """Object Detection class for TensorFlow
    """
    def __init__(self, graph_def, labels):
        super(TFObjectDetection, self).__init__(labels)
        self.graph = tf.Graph()
        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')
            
    def predict(self, preprocessed_image):
        inputs = np.array(preprocessed_image, dtype=np.float)[:,:,(2,1,0)] # RGB -> BGR

        with tf.Session(graph=self.graph) as sess:
            output_tensor = sess.graph.get_tensor_by_name('model_outputs:0')
            outputs = sess.run(output_tensor, {'Placeholder:0': inputs[np.newaxis,...]})
            return outputs[0]

def log_msg(msg):
    print("{}: {}".format(datetime.now(), msg))
    
def initialize():
    print('Loading model...', end='')
    graph_def = tf.GraphDef()
    with tf.gfile.FastGFile(MODEL_FILENAME, 'rb') as f:
        graph_def.ParseFromString(f.read())
    print('Success!')

    print('Loading labels...', end='')
    with open(LABELS_FILENAME, 'r') as f:
        labels = [l.strip() for l in f.readlines()]
    print("{} found. Success!".format(len(labels)))
    
    global od_model
    od_model = TFObjectDetection(graph_def, labels)

def predict_url(image_url):
    log_msg("Predicting from url: " + image_url)
    with urlopen(image_url) as image_binary:
        image = Image.open(image_binary)
        return predict_image(image)
    
def predict_image(image):
    log_msg('Predicting image')

    w, h = image.size
    log_msg("Image size: {}x{}".format(w, h))

    predictions = od_model.predict_image(image)

    response = {
        'id': '',
        'project': '',
        'iteration': '',
        'created': datetime.utcnow().isoformat(),
        'predictions': predictions }
        
    log_msg('Results: ' + str(response))
    return response
