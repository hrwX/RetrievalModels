### pyIR: Collection of Information Retrieval algorithms
[![GitHub version](https://badge.fury.io/gh/hrwx%2FpyIR.svg)](https://badge.fury.io/gh/hrwx%2FpyIR)

A collection of algorithms for querying a set of documents and returning the ones most relevant to the query.

The algorithms that have been implemented are:
- Vector Space Model
- Best Match 25
- Unigram Language Model using Jelinek Mercer Smoothing

## Installation
If you want to be sure you're getting the newest version, you can install it directly from github
```
pip install git+ssh://git@github.com/hrwx/RetrievalModels.git
```

#### TREC
The algorithms were implemented primarily to run evaluations using the TREC Cranfield collection. The TREC evaluation can be run from the `evaluate.py` file.
