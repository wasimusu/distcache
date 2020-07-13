#!/usr/bin/env python
from setuptools import setup

setup(
    name='distcache',
    version='0.1.2',
    author='Wasim Akram Khan',
    keywords='open-source, cache, distributed-cache, in-memory, database',
    description='Distcache is a python open-source distributed in-memory cache and database.',
    packages=['distcache', 'usage', 'benchmark', 'tests'],
    license='MIT License ',
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',
    project_urls={
        "Source Code": "https://github.com/wasimusu/distcache",
    },
    url="https://github.com/wasimusu/distcache",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.7",
    ]
)