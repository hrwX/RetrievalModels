import os
from typing import List, Tuple, dict

import xmltodict


class Importer:
	def __init__(self, path: str) -> None:
		"""
		Imports the files for trec_eval from the path of the specified folder.
		The folder should have two directories
		- COLLECTIONS: contains all the documents.
		- topics: contains all the queries to be searched.
		"""
		self.path = path
		self.collections = []
		self.topics = []

	def load(self) -> Tuple[List[dict], List[dict]]:
		self.load_collections()
		self.load_tokens()

		return self.collections, self.topics

	def load_collections(self):
		try:
			for filename in os.listdir(f"{self.path}/COLLECTION"):
				with open(os.path.join(f"{self.path}/COLLECTION", filename), "r") as file:
					_dict = xmltodict.parse(file.read())
					self.collections.append({
						"id": _dict.get("DOC").get("DOCID"),
						"text": f"{_dict.get('DOC').get('HEADLINE')} {_dict.get('DOC').get('TEXT')}"
					})
		except Exception:
			pass


	def load_tokens(self):
		try:
			for filename in os.listdir(f"{self.path}/topics"):
				with open(os.path.join(f"{self.path}/topics", filename), "r") as file:
					_dict = xmltodict.parse(file.read())
					self.topics.append({
						"id": _dict.get("QUERY").get("QUERYID"),
						"text": f"{_dict.get('QUERY').get('TITLE')} {_dict.get('QUERY').get('DESC')}"
					})
		except Exception:
			pass


