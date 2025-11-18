from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="penguins",
    version="0.3.6",
    include_package_data=True,
    package_data={
        'penguins.data': ['*.csv'],
    },
    python_requires='>=3.8',
    packages=find_packages(),
    install_requires=requirements,
    author="Connor Burruss",
    author_email="cburru2@gmail.com",
    description="A polars addon for dplyr-style methods and functions",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)