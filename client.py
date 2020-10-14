#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import json
from task_serialize import *

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

	


task1 = task()
task1.a = 2
task1.b = 5

j_str = json.dumps(task1, cls=CustomEncoder)

socket.send(bytes(j_str, 'utf-8'))

#  Get the reply.
message = socket.recv()
print("Received reply [ %s ]" % ( message ) )

socket.send(b"kill")

#  Get the reply.
message = socket.recv()
print("Received reply [ %s ]" % ( message ) )