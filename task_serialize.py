import json
import numpy as np
import cv2
import base64

# encode ndarray to base64
def ndarray2base64(img):
	_, im_arr1 = cv2.imencode('.png', img)  # im_arr: image in Numpy one-dim array format.
	im_bytes = im_arr1.tobytes()
	im_b64 = base64.b64encode(im_bytes)
	im_b64_utf8 = im_b64.decode("utf-8")
	return im_b64_utf8

# decode from base64 to ndarray
def base642ndarray(str):
	im_b64 = str.encode("utf-8")
	im_bytes = base64.b64decode(im_b64)
	im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
	img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
	return img

class task(object):
	"""
	задания будут десериализоваться в объект такого класса
	"""
	a = 0
	b = 0
	image = None
	pass

class answer(object):
	"""
	ответы отправляются в таком формате
	"""
	res = 0
	image = None
	pass

# идея взята отсюда, толком не разобрался что именно происходит
# https://code.tutsplus.com/ru/tutorials/serialization-and-deserialization-of-python-objects-part-1--cms-26183
class CustomEncoder(json.JSONEncoder) :
	def default(self, o):
		if isinstance(o, np.ndarray): # картинки opencv в формате np.ndarray
			return {'__base64img__': ndarray2base64(o)}
		return {o.__class__.__name__: o.__dict__}

def decode_object(o):
	if 'task' in o:
		a = task()
		a.__dict__.update(o['task']) # обновляем поля в соответсвии со словарем из json
		return a
	elif 'answer' in o:
		a = answer()
		a.__dict__.update(o['answer'])
		return a
	elif '__base64img__' in o:
		a = base642ndarray(o['__base64img__'])
		return a
	return o
