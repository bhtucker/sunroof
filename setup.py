# -*- coding: utf-8 -*-
"""
    sunroof
    ~~~~~~~

    Packaging
"""
from setuptools import setup, find_packages


def get_requirements(suffix=''):
    with open('requirements%s.txt' % suffix) as f:
        result = f.read().splitlines()
    return result


def get_long_description():
    with open('README', 'r') as f:
        result = f.read()
    return result

setup(
    name='sunroof',
    version='1.0.0',
    url='https://github.com/bhtucker/sunroof',
    author='Benson Tucker',
    author_email='bensontucker@gmail.com',
    description='Ingest some data on congressional data',
    long_description=get_long_description(),
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any'
)
