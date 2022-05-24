from setuptools import setup, find_packages

version = "0.0.1"

setup(
    name="ckanext-repo",
    version=version,
    description="Shows basic information about the CKAN version an instance is running",
    keywords="",
    author="Open Knowledge Foundation",
    author_email="",
    url="http://okfn.org",
    license="AGPL",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    namespace_packages=["ckanext", "ckanext.repo"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points="""
        [ckan.plugins]
        repo_info=ckanext.repo.plugin:RepoInfo
    """,
)
