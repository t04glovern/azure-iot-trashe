from urllib.request import urlopen
from datetime import datetime
import time
import tensorflow as tf
from PIL import Image
import numpy as np
import sys


class Predict():

    def __init__(self):

        self.filename = 'model.pb'
        self.labels_filename = 'labels.txt'
        self.network_input_size = 0
        self.output_layer = 'loss:0'
        self.input_node = 'Placeholder:0'
        self.graph_def = tf.compat.v1.GraphDef()
        self.labels = []
        self.graph = None

        self._initialize()

    def _initialize(self):
        print('Loading model...', end=''),
        with tf.io.gfile.GFile(self.filename, 'rb') as f:
            self.graph_def.ParseFromString(f.read())

        tf.import_graph_def(self.graph_def, name='')
        self.graph = tf.compat.v1.get_default_graph()

        # Retrieving 'network_input_size' from shape of 'input_node'
        input_tensor_shape = self.graph.get_tensor_by_name(
            self.input_node).shape.as_list()

        assert len(input_tensor_shape) == 4
        assert input_tensor_shape[1] == input_tensor_shape[2]

        self.network_input_size = input_tensor_shape[1]

        with open(self.labels_filename, 'rt') as lf:
            self.labels = [l.strip() for l in lf.readlines()]

    def _log_msg(self, msg):
        print("{}: {}".format(time.time(), msg))

    def _resize_to_256_square(self, image):
        w, h = image.size
        new_w = int(256 / h * w)
        image.thumbnail((new_w, 256), Image.ANTIALIAS)
        return image

    def _crop_center(self, image):
        w, h = image.size
        xpos = (w - self.network_input_size) / 2
        ypos = (h - self.network_input_size) / 2
        box = (xpos, ypos, xpos + self.network_input_size,
               ypos + self.network_input_size)
        return image.crop(box)

    def _resize_down_to_1600_max_dim(self, image):
        w, h = image.size
        if h < 1600 and w < 1600:
            return image

        new_size = (1600 * w // h, 1600) if (h > w) else (1600, 1600 * h // w)
        self._log_msg("resize: " + str(w) + "x" + str(h) + " to " +
                      str(new_size[0]) + "x" + str(new_size[1]))
        if max(new_size) / max(image.size) >= 0.5:
            method = Image.BILINEAR
        else:
            method = Image.BICUBIC
        return image.resize(new_size, method)

    def _convert_to_nparray(self, image):
        # RGB -> BGR
        image = np.array(image)
        return image[:, :, (2, 1, 0)]

    def _update_orientation(self, image):
        exif_orientation_tag = 0x0112
        if hasattr(image, '_getexif'):
            exif = image._getexif()
            if exif != None and exif_orientation_tag in exif:
                orientation = exif.get(exif_orientation_tag, 1)
                self._log_msg('Image has EXIF Orientation: ' +
                              str(orientation))
                # orientation is 1 based, shift to zero based and flip/transpose based on 0-based values
                orientation -= 1
                if orientation >= 4:
                    image = image.transpose(Image.TRANSPOSE)
                if orientation == 2 or orientation == 3 or orientation == 6 or orientation == 7:
                    image = image.transpose(Image.FLIP_TOP_BOTTOM)
                if orientation == 1 or orientation == 2 or orientation == 5 or orientation == 6:
                    image = image.transpose(Image.FLIP_LEFT_RIGHT)
        return image

    def predict_url(self, imageUrl):
        self._log_msg("Predicting from url: " + imageUrl)
        with urlopen(imageUrl) as testImage:
            image = Image.open(testImage)
            return self.predict_image(image)

    def predict_image(self, image):
        try:
            if image.mode != "RGB":
                self._log_msg("Converting to RGB")
                image = image.convert("RGB")

            # Update orientation based on EXIF tags
            image = self._update_orientation(image)

            image = self._resize_down_to_1600_max_dim(image)

            image = self._resize_to_256_square(image)

            image = self._crop_center(image)

            cropped_image = self._convert_to_nparray(image)

            with self.graph.as_default():
                with tf.Session() as sess:
                    prob_tensor = sess.graph.get_tensor_by_name(
                        self.output_layer)
                    predictions, = sess.run(
                        prob_tensor, {self.input_node: [cropped_image]})

                    result = []
                    for p, label in zip(predictions, self.labels):
                        truncated_probablity = np.float64(round(p, 8))
                        if truncated_probablity > 1e-8:
                            result.append({
                                'tagName': label,
                                'probability': truncated_probablity,
                                'tagId': '',
                                'boundingBox': None})

                    response = {
                        'id': '',
                        'project': '',
                        'iteration': '',
                        'created': datetime.utcnow().isoformat(),
                        'predictions': result
                    }

                return response

        except Exception as e:
            self._log_msg(str(e))
            return 'Error: Could not preprocess image for prediction. ' + str(e)
