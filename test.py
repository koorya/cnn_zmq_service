import base64
import numpy as np
import cv2
import json
from task_serialize import *

with open("test.jpg", "rb") as f:
	im_b64 = base64.b64encode(f.read()).decode("utf-8")


img = base642ndarray(im_b64)


# cap = cv2.VideoCapture(0)
# _, frame = cap.read()

j_img = json.dumps(img, cls=CustomEncoder)
img_from_j = json.loads(j_img, object_hook=decode_object)

cv2.imshow("lala", img_from_j)
cv2.waitKey(1000)
