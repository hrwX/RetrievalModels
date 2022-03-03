# Copyright (c) 2022, hrwX
# MIT License. See license.txt

from collections import Counter
from math import log
from typing import Dict, List

from RetrievalModels.utils.cache import Cache
from RetrievalModels.utils.inverted_index import InvertedIndex


class JelinekMercerLanguageModel:
	"""
	Unigram Language Model using Jelinek Mercer Smoothing
	"""

	def __init__(self, corpus: Dict[str, List[str]]) -> None:
		self.corpus = corpus
		self.corpus_size = len(self.corpus)
		self.corpus_keys = list(self.corpus.keys())
		self.document_length = []
		self.term_frequency_in_document = []
		self.term_document_frequency_in_corpus = Counter()
		self.inverted_index = InvertedIndex()
		self.total_terms_in_corpus = 0
		self.cache = Cache()

		self._lambda = 0.5

		self.index()

	def index(self) -> None:
		self.calculate_term_and_document_frequencies_and_inverted_index()
		self.calculate_total_terms_in_corpus()

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
			self.term_document_frequency_in_corpus += _frequencies
			self.inverted_index.updatekeys(_frequencies_keys, idx)

	def calculate_total_terms_in_corpus(self) -> None:
		self.total_terms_in_corpus = sum(self.document_length)

	def get_score(self, term: str, term_count_in_query: int, idx: int) -> float:
		score = self.cache.get(f"{idx}:{term}")

		if score is not None:
			return score

		term_count_in_document = (self.term_frequency_in_document[idx] or {}).get(term)
		document_length = self.document_length[idx]
		corpus_frequency = (
			self.term_document_frequency_in_corpus.get(term) /
			self.total_terms_in_corpus
		)

		# fmt: off
		self.cache[f"{idx}:{term}"] = (term_count_in_query) * (
			log(1 + (
					((1 - self._lambda) * (term_count_in_document)) /
					(self._lambda * document_length * corpus_frequency)
				)
			)
		)
		# fmt: on

		return self.cache.get(f"{idx}:{term}")

	def search(self, query: List[str], top_n: int = None) -> List[float]:
		if top_n is None:
			top_n = 10

		score = Counter()

		if top_n == self.corpus_size:
			score = Counter(self.corpus.keys())

		for term in set(query):
			for document_idx in self.inverted_index.get(term, []):
				score[self.corpus_keys[document_idx]] += self.get_score(
					term, query.count(term), document_idx
				)

		return score.most_common(top_n)

