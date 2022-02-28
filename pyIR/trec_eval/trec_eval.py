# Copyright (c) 2022, Himanshu Warekar
# MIT License. See license.txt


from pyIR.best_match_25 import BestMatch25
from pyIR.jelinek_mercer_language_model import JelinekMercerLanguageModel
from pyIR.trec_eval.importer import Importer
from pyIR.vector_space_model import VectorSpaceModel


def evaluate(path: str) -> None:
	importer = Importer(path=path)
	corpus_dict, queries_dict = importer.get()

	top_n = len(corpus_dict)

	best_match_25 = BestMatch25(corpus=corpus_dict)
	vector_space_model = VectorSpaceModel(corpus=corpus_dict)
	language_model = JelinekMercerLanguageModel(corpus=corpus_dict)

	best_match_25_scores = []
	vector_space_model_scores = []
	language_model_scores = []

	for idx, (query_id, query) in enumerate(queries_dict.items()):
		best_match_25_score = best_match_25.search(query=query, top_n=top_n)
		vector_space_model_score = vector_space_model.search(query=query, top_n=top_n)
		language_model_score = language_model.search(query=query, top_n=top_n)

		for idx in range(top_n):
			best_match_25_scores.append(
				f"{query_id} Q0 {best_match_25_score[idx][0]} {idx} {best_match_25_score[idx][1]} nop"
			)
			vector_space_model_scores.append(
				f"{query_id} Q0 {vector_space_model_score[idx][0]} {idx} {vector_space_model_score[idx][1]} nop"
			)
			language_model_scores.append(
				f"{query_id} Q0 {language_model_score[idx][0]} {idx} {language_model_score[idx][1]} nop"
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

