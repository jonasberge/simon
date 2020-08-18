#!/usr/bin/env python

from os import path
from setuptools import setup, find_packages

import simon


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name=simon.__title__,
    author=simon.__author__,
    version=simon.__version__,
    description="A card search bot for the Yu-Gi-Oh! card game",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/vonas/simon',
    keywords='yugioh discord bot',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'discord.py~=1.3',
        'aioredis~=1.3',
        'ZODB~=5.6',
        'RelStorage[postgresql]~=3.2'
    ],
    extras_require={
        'dev': [
            'pytest~=6.0',
            'hypothesis~=5.24',
            'sphinx~=3.2'
        ]
    },
    entry_points={
        'console_scripts': [
            'simon=simon.__main__:main',
        ]
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment :: Board Games',
        'License :: OSI Approved :: %s License' % simon.__license__,
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent'
    ]
)
