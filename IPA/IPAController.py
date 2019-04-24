import IPAModel
import IPAView

class IPAController:
	def __init__(self, model):
		print("IPAController instantiated")		# DEBUG code to delete
		self.model = IPAModel.IPAModel()
		self.view = IPAView.IPAView(self, self.model)

	def start(self):
		self.view.CreateUI()
		self.view.start()