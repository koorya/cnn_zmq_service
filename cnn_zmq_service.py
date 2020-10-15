#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import json
import cv2
from task_serialize import *
from cnn import *

def some_work(task_obj):
	if isinstance(task_obj, task) == False :
		return answer()
	print("a = {}, b = {}, a+b = {}".format(j_obj.a, j_obj.b, j_obj.a + j_obj.b))
	res1 = answer()
	res1.res = j_obj.a + j_obj.b
	return res1

cnn1 = cnn('./cNN/model.json', './cNN/best_weights.h5')

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
message = 0
while message != "kill":
	#  Wait for next request from client
	message = socket.recv().decode('utf-8"')

	try :
		j_obj = json.loads(message, object_hook=decode_object)
		res = some_work(j_obj)
		res.image = cnn1.predict(j_obj.image)
		j_str = json.dumps(res, cls=CustomEncoder)
		socket.send(bytes( j_str, 'utf-8' ))
		continue
	except :
		print("invalid json \n {}".format(message))
		pass

	#  Send reply back to client
	socket.send(b"No command")
