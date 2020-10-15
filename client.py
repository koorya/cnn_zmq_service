#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import json
from task_serialize import *
import cv2

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

	

cap = cv2.VideoCapture(0)
_, frame = cap.read()


task1 = task()
task1.a = 2
task1.b = 5
task1.image = frame

j_str = json.dumps(task1, cls=CustomEncoder)

socket.send(bytes(j_str, 'utf-8'))

#  Get the reply.
message = socket.recv()
try :
	j_obj = json.loads(message, object_hook=decode_object)
	print("res = {}".format(j_obj.res))
except :
	print("invalid json \n {}".format(message))

socket.send(b"kill")

#  Get the reply.
message = socket.recv()
print("Received reply [ %s ]" % ( message ) )