import sys
import argparse
import zmq
import json
from json_coder.py import CustomEncoder, decode_object
from json_coder.py.messages import ServiceTask, CNNTask, CNNAnswer
import cv2

socket_name = "tcp://localhost:5555"

def parseArgs ():
	parser = argparse.ArgumentParser()
	parser.add_argument ('-p', '--port', default='5555')

	return parser.parse_args(sys.argv[1:])

args = parseArgs()
if args.port:
	socket_name = "tcp://localhost:{0}".format(args.port)


context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect(socket_name)

	

cap = cv2.VideoCapture(0)

while 1:
	_, frame = cap.read()

	CNNTask1 = CNNTask()
	CNNTask1.a = 2
	CNNTask1.b = 5
	CNNTask1.image = frame

	j_str = json.dumps(CNNTask1, cls=CustomEncoder)

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


cap.release()
cv2.destroyAllWindows()


kill_task = ServiceTask("kill")
j_str = json.dumps(kill_task, cls=CustomEncoder)
socket.send(bytes(j_str, 'utf-8'))
message = socket.recv().decode('utf-8')
print(message)

