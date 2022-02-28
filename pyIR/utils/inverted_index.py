# Copyright (c) 2022, Himanshu Warekar
# MIT License. See license.txt

from typing import Any, Iterable, Optional


class InvertedIndex(dict):
	def updatekeys(self, __iterable: Iterable, __value: Optional[Any] = None) -> None:
		for __iter in __iterable:
			try:
				self[__iter].append(__value)
			except KeyError:
				self[__iter] = [__value]
