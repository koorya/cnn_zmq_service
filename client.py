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

while 1:
	_, frame = cap.read()

	task1 = task()
	task1.a = 2
	task1.b = 5
	task1.image = frame

	j_str = json.dumps(task1, cls=CustomEncoder)

	socket.send(bytes(j_str, 'utf-8'))

	#  Get the reply.
	message = socket.recv().decode('utf-8')
	try :
		j_obj = json.loads(message, object_hook=decode_object)
		print("res = {}".format(j_obj.res))
		cv2.imshow("client", j_obj.image)
		# cv2.waitKey(5000)

	except :
		print("invalid json \n {}".format(message))

	button_press = cv2.waitKey(1)

	# Нажатие клавиши [q] или [ESC] - завершение работы приложения
	if (button_press & 0xFF == 27) or (button_press & 0xFF == ord('q')) or (button_press & 0xFF == ord('Q')):
		break



socket.send(b"kill")
message = socket.recv()
