from setuptools import setup, find_packages

setup(
	name='vrgaze',
	version="1.1.12",
	url='https://github.com/vrijeuniversiteit/vrgaze.git',
	author='Daniel Müller',
	author_email='d.muller at vu.nl',
	description='Analysis pipelines for virtual reality experiments',
	packages=find_packages(),
	package_data={
		'vrgaze': [
			'example_data/tennis_data/*',
			'example_data/tennis_data/experimental_condition/*',
			'example_data/tennis_data/single_example_file/*'
		]
	},
	install_requires=['matplotlib >= 3.6.2'],
	extras_require={
		'website': ['mkdocs-material>=8.5.11', 'mkdocstrings-python>=0.8.2'],
		'dev': ['pre-commit >= 2.21']
	},
	python_requires=">=3.6",
	classifiers=[
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent",
	],
)
