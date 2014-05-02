#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="opencivicdata",
      version='0.2.0',
      py_modules=['opencivicdata'],
      author="James Turk",
      author_email='jturk@sunlightfoundation.com',
      license="BSD",
      description="python opencivicdata library",
      long_description="",
      url="",
      packages=find_packages(),
      platforms=["any"],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3.3",
                   ],
      )