#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = ['Click>=6.0', 'aiohttp>=3.4.4', 'gera2ld.pyserve']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Gerald",
    author_email='i@gerald.top',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    description="A simple JSON server",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'json_server=json_server.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='json server',
    name='json_server.py',
    packages=find_packages(include=['json_server']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/gera2ld/json_server.py',
    version='0.1.1',
    zip_safe=False,
)
