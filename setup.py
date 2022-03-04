# Copyright (c) 2022, hrwX
# MIT License. See license.txt

import io
import os

from setuptools import find_packages, setup

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")


path = os.path.abspath(os.path.dirname(__file__))
description = "Information Retrival Models"

try:
	with io.open(os.path.join(path, "README.md"), encoding="utf-8") as f:
		long_description = f.read()
except FileNotFoundError:
	long_description = description

setup(
	name="RetrievalModels",
	version="0.0.1",
	description=description,
	long_description=long_description,
	long_description_content_type="text/markdown",
	author="hrwX",
	license="MIT",
	packages=find_packages(),
	py_modules=["RetrievalModels"],
	include_package_data=False,
	zip_safe=False,
	install_requires=install_requires,
)
