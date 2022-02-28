# Copyright (c) 2022, Himanshu Warekar
# MIT License. See license.txt

import os
from string import punctuation
from typing import Dict, List, Optional, Tuple

import xmltodict
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer


class Importer:
	def __init__(self, path: str, language: Optional[str] = None) -> None:
		"""
		Imports the files for trec_eval from the path of the specified folder.
		The folder should have two directories
		- COLLECTIONS: contains all the documents.
		- topics: contains all the queries to be searched.
		"""
		self.path = path
		self.collections = {}
		self.topics = {}
		self.language = language or "english"
		self.stemmer = SnowballStemmer(language=self.language)
		self.stopwords = set(stopwords.words(self.language) + list(punctuation))

	def get(self) -> Tuple[List[Dict], List[Dict]]:
		self.load_collections()
		self.load_tokens()

		return self.collections, self.topics

	def load_collections(self) -> None:
		for filename in os.listdir(f"{self.path}/COLLECTION"):
			with open(os.path.join(f"{self.path}/COLLECTION", filename), "r") as file:
				_dict = xmltodict.parse(file.read())
				text = f"{_dict.get('DOC', {}).get('HEADLINE')} {_dict.get('DOC', {}).get('TEXT')}".lower()
				key = _dict.get("DOC", {}).get("DOCID")

				self.collections.update({key: self.stem(text)})

	def load_tokens(self) -> None:
		for filename in os.listdir(f"{self.path}/topics"):
			with open(os.path.join(f"{self.path}/topics", filename), "r") as file:
				_dict = xmltodict.parse(file.read())
				text = f"{_dict.get('QUERY', {}).get('TITLE')} {_dict.get('QUERY', {}).get('DESC')}".lower()
				key = _dict.get("QUERY", {}).get("QUERYID")

				self.topics.update({key: self.stem(text)})

	def stem(self, corpus: str) -> List[str]:
		return [
			self.stemmer.stem(word)
			for word in corpus.split()
			if word not in self.stopwords
		]
