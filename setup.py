# Copyright (c) 2022, hrwX
# MIT License. See license.txt

from setuptools import find_packages, setup

with open("requirements.txt") as f:
	install_requires = f.read().strip().split('\n')

setup(
	name="RetrievalModels",
	version="0.0.1",
	description="Information Retrival",
	author="hrwX",
	license="MIT",
	packages=find_packages(),
	py_modules=["RetrievalModels"],
	include_package_data=False,
	zip_safe=False,
	install_requires=install_requires
)
