#!/usr/bin/env python3

# BoBoBo

from setuptools import setup, find_packages

setup(
    name='px',
    version='0.1.0-rc.1',
    keywords=("http", "server", "async", "functional"),
    url='https://github.com/engine-py/px.git',
    author='bobobocode',
    author_email='bobobomail@yeah.net',
    description="Async HTTP Server in Python",
    packages=find_packages(exclude=['tests']),
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ]
    },
    include_package_data=True,
    platforms="any",
    license="GPL v3.0"
)
