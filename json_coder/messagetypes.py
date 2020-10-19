


class CNNTask(object):
	"""
	задания будут десериализоваться в объект такого класса
	"""
	a = 0
	b = 0
	image = None
	pass

class CNNAnswer(object):
	"""
	ответы отправляются в таком формате
	"""
	res = 0
	image = None
	pass


class ServiceTask(object):
	command = ""
	def __init__(self, command):
		self.command = command
		pass
	pass

