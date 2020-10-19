from . import utils
from . import classes

def decode_object(o):
	if 'task' in o:
		a = classes.task()
		a.__dict__.update(o['task']) # обновляем поля в соответсвии со словарем из json
		return a
	elif 'answer' in o:
		a = classes.answer()
		a.__dict__.update(o['answer'])
		return a
	elif '__base64img__' in o:
		a = utils.base642ndarray(o['__base64img__'])
		return a
	return o
