# Copyright (c) 2022, Himanshu Warekar
# MIT License. See license.txt

from collections import Counter
from typing import Union


class TweakedCounter(Counter):
	def __mul__(self, __value: Union[int, float]) -> "TweakedCounter":
		return TweakedCounter({key: self[key] * __value for key in self.keys()})

	def __truediv__(self, __value: Union[int, float]) -> "TweakedCounter":
		return TweakedCounter({key: self[key] / __value for key in self.keys()})


