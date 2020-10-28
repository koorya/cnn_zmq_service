#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

from json.decoder import JSONDecodeError
import zmq
import json
import json_coder.py.json_coder as json_coder
from json_coder.py.messagetypes import *
from cnn import *


cnn = Cnn('./cNN/model.json', './cNN/best_weights.h5')

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
message = ""
while True:
	#  Wait for next request from client
	message = socket.recv().decode('utf-8"')


	try:
		task_obj = json.loads(message, object_hook=json_coder.decoder.decode_object)

		if isinstance(task_obj, ServiceTask):
			service_task: ServiceTask = task_obj
			if service_task.command == "kill":
				print("reciev kill command")
				break
		elif isinstance(task_obj, CNNTask):
			cnn_task: CNNTask = task_obj
			answer: CNNAnswer = CNNAnswer()
			answer.image = cnn.predict(cnn_task.image)
			answer_str = json.dumps(answer, cls=json_coder.coder.CustomEncoder)
			socket.send(bytes( answer_str, 'utf-8' ))
			continue
	except JSONDecodeError:
		print("invalid json \n {}".format(message))
		error_answer = ServiceTask()
		error_answer.command = "Illegal json"
		answer_str = json.dumps(error_answer, cls=json_coder.coder.CustomEncoder)
		socket.send(bytes( answer_str, 'utf-8' ))
		continue



	#  Send reply back to client
	socket.send(b"No command")
