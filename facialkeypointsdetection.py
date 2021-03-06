# -*- coding: utf-8 -*-
"""FacialKeypointsDetection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m2uaffjRBIC3WlkaK7hVEW6vw3EgRTN1
"""

import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

model = load_model('model/facialKeyPointsDetection.h5')

# haarcascade_frontalface for face detecting
haarcascade_path = "assets/haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(haarcascade_path)

image = cv2.imread('assets/people_with_phones.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.3,
    minNeighbors=3,
    minSize=(30,30)
)
print(f"found {len(faces)} faces.")

for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    
    roi_color = image[y:y+h, x:x+w]

    roi_gray = cv2.cvtColor(roi_color, cv2.COLOR_BGR2GRAY)

    resized_image = cv2.resize(roi_gray, (96, 96))

    img_model = np.reshape(resized_image, (1, 96, 96, 1))
    keypoints = model.predict(img_model)

    keypoints = np.reshape(keypoints, 30)

    x_coords = []
    y_coords = []

    for i in range(len(keypoints)):
        if i % 2 == 0:
            x_coords.append(keypoints[i])
        else:
            y_coords.append(keypoints[i])

    for i in range(len(x_coords)):          # Plot the keypoints at the x and y coordinates
        cv2.circle(resized_image, (x_coords[i], y_coords[i]), 2, (255,255,0), -1)
    cv2.imshow(resized_image)

