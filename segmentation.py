import numpy as np
import matplotlib.pyplot as plt
import cv2
import pandas as pd
import tf_keras as k3

import keras
from keras.applications.resnet import ResNet50
from keras.applications.vgg16 import VGG16
from keras.models import Model, load_model

import matplotlib.image

def segmentation(input, output):
    model = k3.models.load_model("my_model_v11")

    image = cv2.imread(input)
    
#    (w, h) = image.shape[:-1]
    
    image = cv2.resize(image, (256, 256))
    matplotlib.image.imsave(input, image)
    pred = model.predict(np.array([image]))
    image_output = pred[0, ..., 0] > 0.5
#    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(25, 25))
#    axes[0].imshow(image)
#    axes[1].imshow(image_output)
#    plt.show()

    matplotlib.image.imsave(output, image_output)