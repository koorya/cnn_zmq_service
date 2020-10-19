#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import json
import cv2
import json_coder.json_coder as json_coder
from cnn import *

def some_work(task_obj):
	if isinstance(task_obj, json_coder.classes.task) == False :
		return json_coder.classes.answer()
	print("a = {}, b = {}, a+b = {}".format(j_obj.a, j_obj.b, j_obj.a + j_obj.b))
	res1 = json_coder.classes.answer()
	res1.res = j_obj.a + j_obj.b
	return res1

cnn = Cnn('./cNN/model.json', './cNN/best_weights.h5')

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
message = 0
while message != "kill":
	#  Wait for next request from client
	message = socket.recv().decode('utf-8"')

	try :
		j_obj = json.loads(message, object_hook=json_coder.decoder.decode_object)
		res = some_work(j_obj)
		res.image = cnn.predict(j_obj.image)
		j_str = json.dumps(res, cls=json_coder.coder.CustomEncoder)
		socket.send(bytes( j_str, 'utf-8' ))
		continue
	except :
		print("invalid json \n {}".format(message))
		pass

	#  Send reply back to client
	socket.send(b"No command")
