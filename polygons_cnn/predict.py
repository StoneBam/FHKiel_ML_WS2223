import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

IMG_WIDHT = 128
IMG_HEIGHT = 128

DATA_DIR = os.path.join(os.path.dirname(__file__), ".data/polygons_data")
CLASS_NAMES = ['hexagon', 'pentagon', 'square', 'triangle']


if __name__ == '__main__':
    model: tf.keras.Model = tf.keras.models.load_model(os.path.join(DATA_DIR, 'model.h5'))
    model.summary()

    while True:
        img = tf.keras.utils.load_img(
            os.path.join(DATA_DIR, "test.png"), target_size=(IMG_WIDHT, IMG_HEIGHT)
        )
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create a batch

        predictions = model.predict(img_array)
        print(predictions)
        score = tf.nn.softmax(predictions[0])
        print(score)

        print(f"This image most likely belongs to {CLASS_NAMES[np.argmax(score)]} with a {100 * np.max(score):.2f} percent confidence.")

        plt.figure(figsize=(10, 6))
        plt.subplot(1, 2, 1)
        plt.title('Picture')
        plt.imshow(img)
        plt.subplot(1, 2, 2)
        plt.title('Prediction')
        plt.bar(CLASS_NAMES, score)
        plt.show()
        input()
