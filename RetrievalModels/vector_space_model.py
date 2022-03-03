# Copyright (c) 2022, hrwX
# MIT License. See license.txt

from collections import Counter
from math import log, sqrt
from typing import Dict, Hashable, List

from RetrievalModels.utils.cache import Cache
from RetrievalModels.utils.collections import TweakedCounter
from RetrievalModels.utils.inverted_index import InvertedIndex


class VectorSpaceModel:
	"""
	Vector Space Model using Inverted Index
	"""

	def __init__(self, corpus: Dict[str, List[str]]) -> None:
		self.corpus = corpus
		self.corpus_size = len(self.corpus)
		self.corpus_keys = list(self.corpus.keys())
		self.term_frequency_in_document = []
		self.term_document_frequency_in_corpus = Counter()
		self.inverse_document_frequency = TweakedCounter()
		self.term_frequency_inverse_document_frequency = []
		self.inverted_index = InvertedIndex()
		self.cache = Cache()

		self.index()

	def index(self) -> None:
		self.calculate_term_and_document_frequencies_and_inverted_index()
		self.calculate_inverse_document_frequency()
		self.calculate_term_frequency_inverse_document_frequency()

	def calculate_term_and_document_frequencies_and_inverted_index(self) -> None:
		"""
		Calculates the term frequency in the document
		Calculates the term frequency in the collection
		Builds the Inverted Index for retrival
		"""
		for idx, document in enumerate(self.corpus.values()):
			_frequencies = TweakedCounter(document) / len(document)
			_frequencies_keys = _frequencies.keys()

			self.term_frequency_in_document.append(_frequencies)
			self.term_document_frequency_in_corpus += Counter(_frequencies_keys)
			self.inverted_index.updatekeys(_frequencies_keys, idx)

	def calculate_inverse_document_frequency(self) -> None:
		"""
		Calculates the inverse document frequency
		"""
		for term, frequency in self.term_document_frequency_in_corpus.items():
			self.inverse_document_frequency[term] = log(self.corpus_size / frequency)

	def calculate_term_frequency_inverse_document_frequency(self) -> None:
		"""
		Calculates the term frequency inverse document frequency
		"""
		for term_frequency in self.term_frequency_in_document:
			_term_frequency = term_frequency

			for term in term_frequency:
				_term_frequency[term] *= self.inverse_document_frequency.get(term)

			self.term_frequency_inverse_document_frequency.append(_term_frequency)

	def get_root_sum_square_from_cache(
		self, frequency: Dict[str, int], key: Hashable
	) -> float:
		"""
		Computes the root sum of squares or fetches it from cache
		"""
		root_sum_square = self.cache.get(key)

		if root_sum_square is not None:
			return root_sum_square

		self.cache[key] = sqrt(sum([term**2 for term in frequency.values()]))
		return self.cache.get(key)

	def get_score(self, query: List[str], idx: int) -> float:
		document = self.term_frequency_inverse_document_frequency[idx] or {}
		common_terms = set(query) & set(document)

		document_root_sum_square = self.get_root_sum_square_from_cache(document, idx)
		query_root_sum_square = self.get_root_sum_square_from_cache(query, tuple(query))

		return sum(
			[document.get(term, 0) * query.get(term, 0) for term in common_terms]
		) / (document_root_sum_square * query_root_sum_square)

	def search(self, query: List[str], top_n: int = None) -> List[float]:
		if top_n is None:
			top_n = 10

		query = Counter(query)
		score = Counter()

		if top_n == self.corpus_size:
			score = Counter(self.corpus.keys())

		for term in set(query):
			for document_idx in self.inverted_index.get(term, []):
				score[self.corpus_keys[document_idx]] += self.get_score(
					query, document_idx
				)

		return score.most_common(top_n)

