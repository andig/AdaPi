#!/usr/bin/env python

from distutils.core import setup

setup(name='adapi',
      version='0.1',
      description='Python port of various libraries for use with the Raspberry Pi',
      author='Andreas Goetz',
      author_email='cpudile@gmx.de',
      url='http://github.com/andig/AdaPi/',
      long_description=open('README.md').read(),
      packages=['adafruit', 'gaugette', 'fonts'],
)