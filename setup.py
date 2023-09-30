from setuptools import setup, find_packages

# Package metadata
name = "preloader"
version = "0.1"
description = "A simple Python preloader package"
author = "Andres Gonzalez"
author_email = "code@andresgz.com"
url = "https://github.com/andresgz/preloader"

classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

install_requires = [
    "requests",  # Example dependency
    "beautifulsoup4",
    "validators",
    "lxml"
]


setup(
    name=name,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    packages=find_packages(),
    classifiers=classifiers,
    install_requires=install_requires,  # Specify dependencies here
)
