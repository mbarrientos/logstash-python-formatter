#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

from setuptools import find_packages

import logstash

with open('requirements.txt', 'r') as f:
    requires = f.read().splitlines()

setup(
    name='logstash-python-formatter',
    version=logstash.__version__,
    author=logstash.__author__,
    license=logstash.__license__,
    url=logstash.__url__,
    description=logstash.__description__,
    long_description='\n'.join([open('README.md').read()]),
    keywords='python, logging, logstash, formatter, log',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        # Environment
        'Environment :: Web Environment',
        # Intended Audience:
        'Intended Audience :: Support',
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
    test_suite='logstash.tests',
    tests_require=['tox', 'six'],
)
