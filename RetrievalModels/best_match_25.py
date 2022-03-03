# Copyright (c) 2022, hrwX
# MIT License. See license.txt

from collections import Counter
from math import log
from typing import Dict, List

from RetrievalModels.utils.cache import Cache
from RetrievalModels.utils.inverted_index import InvertedIndex


class BestMatch25:
	"""
	Best Match 25
	"""

	def __init__(self, corpus: Dict[str, List[str]]) -> None:
		self.corpus = corpus
		self.corpus_size = len(self.corpus)
		self.corpus_keys = list(self.corpus.keys())
		self.document_length = []
		self.average_document_length = 0
		self.term_frequency_in_document = []
		self.term_document_frequency_in_corpus = Counter()
		self.inverse_document_frequency = dict()
		self.inverted_index = InvertedIndex()
		self.cache = Cache()

		self.k1 = 1.2
		self.b = 0.75

		self.index()

	def index(self) -> None:
		self.calculate_term_and_document_frequencies_and_inverted_index()
		self.calculate_inverse_document_frequency()
		self.calculate_average_document_length()

	def calculate_term_and_document_frequencies_and_inverted_index(self) -> None:
		"""
		Calculates the term frequency in the document
		Calculates the term frequency in the collection
		Builds the Inverted Index for retrival
		"""
		for idx, document in enumerate(self.corpus.values()):
			self.document_length.append(len(document))

			_frequencies = Counter(document)
			_frequencies_keys = _frequencies.keys()

			self.term_frequency_in_document.append(_frequencies)
			self.term_document_frequency_in_corpus += Counter(_frequencies_keys)
			self.inverted_index.updatekeys(_frequencies_keys, idx)

	def calculate_inverse_document_frequency(self) -> None:
		"""
		Calculates the inverse document frequency
		"""
		for term, frequency in self.term_document_frequency_in_corpus.items():
			self.inverse_document_frequency[term] = log(
				((self.corpus_size - frequency + 0.5) / (frequency + 0.5)) + 1
			)

	def calculate_average_document_length(self) -> None:
		self.average_document_length = sum(self.document_length) / self.corpus_size

	def get_score(self, term: str, idx: int) -> float:
		document_length = self.document_length[idx] or 0
		term_frequency_in_document = self.term_frequency_in_document[idx] or {}

		score = self.cache.get(f"{idx}:{term}")

		if score is not None:
			return score

		frequency = term_frequency_in_document.get(term)
		# fmt: off
		_term_frequency = (
			(frequency * (self.k1 + 1)) /
			(frequency + self.k1 * (1 - self.b + (self.b * document_length / self.average_document_length)))
		)
		# fmt: on

		self.cache[f"{idx}:{term}"] = (
			self.inverse_document_frequency.get(term) * _term_frequency
		)

		return self.cache.get(f"{idx}:{term}")

	def search(self, query: List[str], top_n: int = None) -> List[float]:
		if top_n is None:
			top_n = 10

		query = set(query)
		score = Counter()

		if top_n == self.corpus_size:
			score = Counter(self.corpus.keys())

		for term in query:
			for document_idx in self.inverted_index.get(term, []):
				score[self.corpus_keys[document_idx]] += self.get_score(
					term, document_idx
				)

		return score.most_common(top_n)

