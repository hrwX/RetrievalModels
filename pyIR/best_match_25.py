import math
from collections import Counter
from typing import Dict, List, Optional

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# import numpy as np


class BM25:
	"""
	Best Match 25.

	Parameters
	----------
	k1 : float, default 1.5

	b : float, default 0.75

	Attributes
	----------
	tf_ : list[dict[str, int]]
		Term Frequency per document. So [{'hi': 1}] means
		the first document contains the term 'hi' 1 time.

	df_ : dict[str, int]
		Document Frequency per term. i.e. Number of documents in the
		corpus that contains the term.

	idf_ : dict[str, float]
		Inverse Document Frequency per term.

	doc_len_ : list[int]
		Number of terms per document. So [3] means the first
		document contains 3 terms.

	corpus_ : list[list[str]]
		The input corpus.

	corpus_size_ : int
		Number of documents in the corpus.

	avg_doc_len_ : float
		Average number of terms for documents in the corpus.
	"""

	def __init__(self, collections: List[Dict], tokens: Optional[List[Dict]]):
		self.collections = collections
		self.collections_size = len(self.collections)
		self.tokens = tokens
		self.dl = []
		self.avgerage_dl = 0
		self.f = []
		self.df = Counter()
		self.idf = Counter()
		self.average_idf = 0
		self.cache = Counter()

		self.k1 = 1.2
		self.b = 0.75

	def initialize(self):
		for document in self.collections:
			document = document.get("text").split(" ")
			self.dl.append(len(document))
			_frequencies = Counter(document)
			self.f.append(_frequencies)
			self.df += _frequencies

		for word, frequency in self.df.items():
			self.idf[word] = math.log((self.collections_size - frequency + 0.5) - (frequency + 0.5))

		self.avgerage_dl = sum(self.dl) / len(self.dl)
		self.average_idf = sum(self.idf.values()) / len(self.idf)

	def _score(self, query, idx):
		score = 0
		dl = self.dl[idx]
		frequencies = self.f[idx]

		for word in query:
			if word not in frequencies:
				continue

			f = frequencies[word]
			score += (self.df[word] * f * (self.k1 + 1)) / (f + self.k1 * (1 - self.b + (self.b * dl / self.avgerage_dl)))

		return score

	def search(self, query):
		query = query.get("text").split(" ")
		score = []
		for idx in range(self.collections_size):
			_score = self._score(query, idx)
			score.append({
				"query_id": query.get("id"),

			})


	def evaluate_for_trec_eval(self):
		pass
