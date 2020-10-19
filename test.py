import base64
import numpy as np
import cv2
import json
from CNNTask_serialize import *
from cnn import *

with open("test.jpg", "rb") as f:
	im_b64 = base64.b64encode(f.read()).decode("utf-8")


img = base642ndarray(im_b64)


j_img = json.dumps(img, cls=CustomEncoder)
img_from_j = json.loads(j_img, object_hook=decode_object)

cv2.imshow("lala 1", img_from_j)
cv2.waitKey(1000)


cnn1 = cnn('./cNN/model.json', './cNN/best_weights.h5')
img = cnn1.predict(img)

cv2.imshow("test", img)
cv2.waitKey(1000)

# cap = cv2.VideoCapture(0)
# _, frame = cap.read()

j_img = json.dumps(img, cls=CustomEncoder)
img_from_j = json.loads(j_img, object_hook=decode_object)

cv2.imshow("lala", img_from_j)
cv2.waitKey(1000)
