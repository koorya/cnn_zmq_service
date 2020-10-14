import json

class task(object):
	"""
	задания будут десериализоваться в объект такого класса
	"""
	a = 0
	b = 0

	pass

class answer(object):
	"""
	ответы отправляются в таком формате
	"""
	res = 0
	pass

# идея взята отсюда, толком не разобрался что именно происходит
# https://code.tutsplus.com/ru/tutorials/serialization-and-deserialization-of-python-objects-part-1--cms-26183
class CustomEncoder(json.JSONEncoder) :
	def default(self, o):
		return {o.__class__.__name__: o.__dict__}

def decode_object(o):
	if 'task' in o:
		a = task()
		a.__dict__.update(o['task'])
		return a
	elif 'answer' in o:
		a = answer()
		a.__dict__.update(o['answer'])
		return a
	return o
