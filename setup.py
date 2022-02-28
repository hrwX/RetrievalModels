# Copyright (c) 2022, Himanshu Warekar
# MIT License. See license.txt

from setuptools import find_packages, setup

with open("requirements.txt") as f:
	install_requires = f.read().strip().split('\n')

setup(
	name="pyIR",
	version="0.0.1-alpha",
	description="Information Retrival",
	author="Himanshu Warekar",
	license="MIT",
	packages=find_packages(),
	py_modules=["pyIR"],
	include_package_data=False,
	zip_safe=False,
	install_requires=install_requires
)
