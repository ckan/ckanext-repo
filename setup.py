from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(
	name='ckanext-repo',
	version=version,
	description='Shows basic information about the CKAN version an instance is running',
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Open Knowledge Foundation',
	author_email='',
	url='http://okfn.org',
	license='AGPL',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.repo'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
        [ckan.plugins]
	# Add plugins here, eg
	repo_info=ckanext.repo.plugin:RepoInfo
	""",
)
