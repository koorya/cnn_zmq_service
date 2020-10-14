import json

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
