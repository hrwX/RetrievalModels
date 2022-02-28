# Copyright (c) 2022, Himanshu Warekar
# MIT License. See license.txt

import json

from pyIR.best_match_25 import BestMatch25
from pyIR.jelinek_mercer_language_model import JelinekMercerLanguageModel
from pyIR.trec_eval.importer import Importer
from pyIR.vector_space_model import VectorSpaceModel


def evaluate(path: str) -> None:
	importer = Importer(path=path)
	corpus_dict, queries_dict = importer.get()

	with open(f"{path}/corpus.json") as f:
		corpus_dict = json.load(f)

	with open(f"{path}/query.json") as f:
		queries_dict = json.load(f)

	corpus_keys = list(corpus_dict.keys())
	corpus_values = list(corpus_dict.values())

	best_match_25 = BestMatch25(corpus=corpus_values)
	vector_space_model = VectorSpaceModel(corpus=corpus_values)
	language_model = JelinekMercerLanguageModel(corpus=corpus_values)

	best_match_25_scores = []
	vector_space_model_scores = []
	language_model_scores = []

	corpus_length = len(corpus_dict)

	for idx, (query_id, query) in enumerate(queries_dict.items()):
		best_match_25_score = best_match_25.search(query)
		vector_space_model_score = vector_space_model.search(query)
		language_model_score = language_model.search(query)

		for idx in range(corpus_length):
			best_match_25_scores.append(
				f"{query_id} Q0 {corpus_keys[idx]} {idx} {best_match_25_score[idx]} nop"
			)
			vector_space_model_scores.append(
				f"{query_id} Q0 {corpus_keys[idx]} {idx} {vector_space_model_score[idx]} nop"
			)
			language_model_scores.append(
				f"{query_id} Q0 {corpus_keys[idx]} {idx} {language_model_score[idx]} nop"
			)


	output_map = {
		"best_match_25.txt": best_match_25_scores,
		"vector_space_model.txt": vector_space_model_scores,
		"language_model.txt": language_model_scores,
	}

	for filename, scores in output_map.items():
		with open(f"{path}/{filename}", "w") as filename:
			filename.writelines("\n".join(scores))
			filename.close()

