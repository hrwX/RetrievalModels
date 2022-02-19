from simplejson import OrderedDict


class Document:
	def __init__(self, document: OrderedDict):
		self.document = document
