class NotImplemented(Exception):
	pass

class DoesNotExist(Exception):
	def __init__(self):
		super.__init__("Path doesn't exist.")

class FileDoesNotExist(Exception):
	def __init__(self):
		super.__init__("File doesn't exist.")
