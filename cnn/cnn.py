import json
import cv2
import numpy as np
import tensorflow as tf

class Cnn():
	model = None

	def __init__(self, model_path, weights_path):
		tf.compat.v1.reset_default_graph()
		tf.compat.v1.set_random_seed(13)
		np.random.seed(13)

		### https://forums.developer.nvidia.com/t/could-not-create-cudnn-handle-cudnn-status-alloc-failed/108261/3
		gpus = tf.config.experimental.list_physical_devices('GPU')
		if gpus:
			try:
				# Currently, memory growth needs to be the same across GPUs
				for gpu in gpus:
					tf.config.experimental.set_memory_growth(gpu, True)
					logical_gpus = tf.config.experimental.list_logical_devices('GPU')
					print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
			except RuntimeError as e:
				# Memory growth must be set before GPUs have been initialized
				print(e)
		### ____________________________________________________________________________

		with open(model_path) as json_file:
			data = json.load(json_file)

		self.model = tf.keras.models.model_from_json(data)
		self.model.load_weights(weights_path)

	def predict(self, img):
		frame = img 
		gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
		h, w = gray.shape
		min_dim = min(h, w)
		hc = int((h - min_dim) / 2)
		wc = int((w - min_dim) / 2)
		gray_resized = cv2.resize( gray[hc:(hc + min_dim), wc:(wc + min_dim)], (512, 512), interpolation=cv2.INTER_AREA )
		gray = cv2.cvtColor( gray_resized , cv2.COLOR_GRAY2RGB ) / 255.0 
		view_gray = gray.copy() 
		predict_gray = gray.reshape((-1, 512, 512, 3))
		result = self.model.predict(predict_gray, verbose=1)
		result = result.reshape((512, 512, -1))
		to_save = np.hstack((view_gray, cv2.cvtColor(result, cv2.COLOR_BGR2RGB)))
		return (to_save*255).astype('uint8')