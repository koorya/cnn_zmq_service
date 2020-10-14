#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import json

from task_serialize import *

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
message = 0
while message != b"kill":
	#  Wait for next request from client
	message = socket.recv()
	print("Received request: %s" % message)

	try :
		j_obj = json.loads(message, object_hook=decode_object)
		print("a = {}, b = {}, a+b = {}".format(j_obj.a, j_obj.b, j_obj.a + j_obj.b))
	except :
		print("invalid json \n {}".format(message))
	#  Do some 'work'
	time.sleep(0.1)

	#  Send reply back to client
	socket.send(b"World")
