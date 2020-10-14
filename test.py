import base64
import numpy as np
import cv2

with open("test.jpg", "rb") as f:
	im_b64 = base64.b64encode(f.read())


im_bytes = base64.b64decode(im_b64)
im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)


cap = cv2.VideoCapture(0)
_, frame = cap.read()


# encode ndarray to base64
def ndarray2base64(img):
	_, im_arr1 = cv2.imencode('.png', img)  # im_arr: image in Numpy one-dim array format.
	im_bytes = im_arr1.tobytes()
	im_b64 = base64.b64encode(im_bytes)
	return im_b64

# decode from base64 to ndarray
def base642ndarray(str):
	im_bytes = base64.b64decode(str)
	im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
	img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
	return img

cv2.imshow("lala", base642ndarray(ndarray2base64(img)))
cv2.waitKey(1000)
