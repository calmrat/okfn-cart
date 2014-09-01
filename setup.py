#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward" <cward@redhat.com>

from setuptools import setup, Extension


__pkg__ = 'cart'
__pkgs__ = ['cart']
__provides__ = ['cart']
__desc__ = 'OKFN Cart Excersize'

with open('README.rst') as _file:
    readme = _file.read()

github = 'https://github.com/kejbaly2/okfn_cart'

default_setup = dict(
    url=github,
    license='GPLv3',
    author='Chris Ward',
    author_email='cward@redhat.com',
    long_description=readme,
    description=__desc__,
    name=__pkg__,
    packages=__pkgs__,
    provides=__provides__,
)

setup(**default_setup)
