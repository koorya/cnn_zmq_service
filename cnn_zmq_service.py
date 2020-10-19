#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

from json.decoder import JSONDecodeError
import zmq
import json
import json_coder.json_coder as json_coder
from json_coder.messagetypes import *
from cnn import *


def additionalWork(task_obj: CNNTask):
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


	try:
		j_obj = json.loads(message, object_hook=json_coder.decoder.decode_object)

		if isinstance(j_obj, ServiceTask):
			service_task: ServiceTask = j_obj
			if service_task.command == "kill":
				break
		elif isinstance(j_obj, CNNTask):
			cnn_task: CNNTask = j_obj
			answer: CNNAnswer = CNNAnswer()
			answer.b = additionalWork(cnn_task)
			answer.image = cnn.predict(cnn_task.image)
			j_str = json.dumps(answer, cls=json_coder.coder.CustomEncoder)
			socket.send(bytes( j_str, 'utf-8' ))
			continue
	except JSONDecodeError:
		print("invalid json \n {}".format(message))
		socket.send(b"Illegal json")
		continue



	#  Send reply back to client
	socket.send(b"No command")
