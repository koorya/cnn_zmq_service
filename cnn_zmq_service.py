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

def additionalWork(task_obj: json_coder.classes.CNNTask):
	print("a = {}, b = {}, a+b = {}".format(task_obj.a, task_obj.b, task_obj.a + task_obj.b))
	return task_obj.a + task_obj.b

cnn = Cnn('./cNN/model.json', './cNN/best_weights.h5')

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
message = ""
while True:
	#  Wait for next request from client
	message = socket.recv().decode('utf-8"')

	j_obj = None

	try:
		j_obj = json.loads(message, object_hook=json_coder.decoder.decode_object)
	except :
		print("invalid json \n {}".format(message))

	if isinstance(j_obj, json_coder.classes.ServiceTask):
		j_obj: json_coder.classes.ServiceTask = j_obj
		if j_obj.command == "kill":
			break

	elif isinstance(j_obj, json_coder.classes.CNNTask):
		cnn_task: json_coder.classes.CNNTask = j_obj
		res: json_coder.classes.CNNAnswer = json_coder.classes.CNNAnswer()
		res.b = additionalWork(cnn_task)
		res.image = cnn.predict(cnn_task.image)
		j_str = json.dumps(res, cls=json_coder.coder.CustomEncoder)
		socket.send(bytes( j_str, 'utf-8' ))
		continue


	#  Send reply back to client
	socket.send(b"No command")
