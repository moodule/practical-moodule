#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'beautifulsoup4>=4.6.3',
    'decorator>=4.3.0',
    'lxml>=4.2.5',
    'numpy>=1.14.2',
    'sh>=1.12.4',
    'sympy>=1.1.1',
    # TODO: put package requirements here
]

setup_requirements = [
    'bumpversion>=0.5.3',
    'Sphinx>=1.4.8',
    'watchdog>=0.8.3',
    'wheel>=0.29.0',
    # TODO(moodule): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'coverage>=4.1'
    'flake8>=2.6.0',
    'pytest>=2.9.2',
    'pytest-runner>=2.11.1',
    'tox>=2.3.1',
    # TODO: put package test requirements here
]

setup(
    name='practical',
    version='0.4.2',
    description="Personal toolbox.",
    long_description=readme + '\n\n' + history,
    author="David Mougeolle",
    author_email='david.mougeolle@moodule.net',
    url='https://github.com/moodule/practical-moodule',
    packages=find_packages(include=['practical']),
    entry_points={
        'console_scripts': [
            'practical=practical.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='practical',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
