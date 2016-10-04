#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

import sys
from setuptools import find_packages

import logstash_formatter

if sys.version_info[0] == 2:
    from codecs import open

with open('requirements.txt', 'r') as f:
    requires = f.read().splitlines()

setup(
    name='logstash-python-formatter',
    version=logstash_formatter.__version__,
    author=logstash_formatter.__author__,
    license=logstash_formatter.__license__,
    url=logstash_formatter.__url__,
    description=logstash_formatter.__description__,
    long_description='\n'.join([open('README.rst', encoding='utf-8').read()]),
    keywords='python, logging, logstash_formatter, formatter, log',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        # Environment
        'Environment :: Web Environment',
        # Intended Audience:
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        # License
        'License :: OSI Approved :: MIT License',
        # Natural Language
        'Natural Language :: English',
        # Operating System
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        # Programming Language
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        # Topic
        'Topic :: Software Development',
        'Topic :: Software Development :: Bug Tracking',
        'Topic :: System :: Logging',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    test_suite='tests',
    tests_require=['tox', 'six'],
)
