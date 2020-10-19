from . import utils
from . import classes

def decode_object(o):
	if 'CNNTask' in o:
		a = classes.CNNTask()
		a.__dict__.update(o['CNNTask']) # обновляем поля в соответсвии со словарем из json
		return a
	elif 'CNNAnswer' in o:
		a = classes.CNNAnswer()
		a.__dict__.update(o['CNNAnswer'])
		return a
	elif 'ServiceTask' in o:
		a = classes.ServiceTask("")
		a.__dict__.update(o['ServiceTask'])
		return a
	elif '__base64img__' in o:
		a = utils.base642ndarray(o['__base64img__'])
		return a
	return o
