import sys
import argparse
from json.decoder import JSONDecodeError
import zmq
import json
from json_coder import * 
from cnn.cnn import *

cnn_model = './cnn/config/model.json' # граф нейросети
cnn_weight = './cnn/config/best_weights.h5' # веса нейросети
socket_name = "tcp://*:5555"

def parseArgs ():
	parser = argparse.ArgumentParser()
	parser.add_argument ('-p', '--port', default='5555')

	return parser.parse_args(sys.argv[1:])

args = parseArgs()
if args.port:
	socket_name = "tcp://*:{0}".format(args.port)

cnn = Cnn(cnn_model, cnn_weight)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(socket_name)
message = ""
while True:
	#  Wait for next request from client
	message = socket.recv().decode('utf-8"')


	try:
		task_obj = json.loads(message, object_hook=decode_object)

		if isinstance(task_obj, ServiceTask):
			service_task: ServiceTask = task_obj
			if service_task.command == "kill":
				print("reciev kill command")
				break
		elif isinstance(task_obj, CNNTask):
			cnn_task: CNNTask = task_obj
			answer: CNNAnswer = CNNAnswer()
			answer.image = cnn.predict(cnn_task.image)
			answer_str = json.dumps(answer, cls=CustomEncoder)
			socket.send(bytes( answer_str, 'utf-8' ))
			continue
	except JSONDecodeError:
		print("invalid json \n {}".format(message))
		error_answer = ServiceTask()
		error_answer.command = "Illegal json"
		answer_str = json.dumps(error_answer, cls=CustomEncoder)
		socket.send(bytes( answer_str, 'utf-8' ))
		continue



	#  Send reply back to client
	defualt_answer = ServiceTask()
	defualt_answer.command = "Illegal command"
	answer_str = json.dumps(defualt_answer, cls=CustomEncoder)
	socket.send(bytes( answer_str, 'utf-8' ))

