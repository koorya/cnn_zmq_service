#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import json
import pprint
context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

	
class task :
	a = 0
	b = 0

class CustomEncoder(json.JSONEncoder) :
	def default(self, o):
		return {'__{}__'.format(o.__class__.__name__): o.__dict__}

def decode_object(o):
	if '__task__' in o:
		a = task()
		a.__dict__.update(o['__task__'])
		return a
	return o


task1 = task()
task1.a = 2
task1.b = 5

j_str = json.dumps(task1, cls=CustomEncoder)
j_obj = json.loads(j_str, object_hook=decode_object)
pprint.pprint(j_obj) 
print("a = {}, b = {}".format(j_obj.a, j_obj.b))

exit()

socket.send(b"kill")

#  Get the reply.
message = socket.recv()
print("Received reply [ %s ]" % ( message ) )