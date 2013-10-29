# -*- coding: utf-8 -*-
#
#  setup.py
#  hipchav
#

from setuptools import setup

VERSION = '0.1.1'

setup(
    name='hipchav',
    description="A minimal command-line HipChat client.",
    long_description=open('README.rst').read(),
    url="https://github.com/larsyencken/hipchav/",
    version=VERSION,
    author="Lars Yencken",
    author_email="lars@yencken.org",
    license="ISC",
    scripts=['hipchav.py'],
    packages=[],
    install_requires=['requests>=1.2.3'],
)
