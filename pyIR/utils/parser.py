from multiprocessing import set_forkserver_preload
import xmltodict
import os

class Parser:
	def __init__(self, path: str) -> None:
		self.path = path
		self.documents = []
		self.validate_path()
		self.parse()

	def validate_path(self):
		if not self.path.endswith("/"):
			self.path += "/"

	def parse(self):
		for xmlfile in os.listdir(self.path):
			with open(self.get_path(xmlfile)) as f:
				_dict = xmltodict(f.read())
				self.documents.append(_dict)
				f.close()

	def get_path(self, filename):
		return f"{self.path}{filename}"

	def get_documents(self):
		return self.documents

