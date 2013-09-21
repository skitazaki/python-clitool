from setuptools import setup, find_packages
import sys, os

import clitool

with open('README.txt') as file:
    long_description = file.read()

setup(name='clitool',
      version=clitool.__version__,
      description="Command Line Script Support Utility",
      long_description=long_description,
      classifiers=[ # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education"
      ],
      keywords='',
      author='KITAZAKI Shigeru',
      author_email='skitazaki@gmail.com',
      url='https://github.com/skitazaki/python-clitool-template',
      license='Apache',
      #packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      packages=['clitool'],
      package_dir={'clitool': 'clitool'},
      include_package_data=False,
      zip_safe=False,
      install_requires=[
        'six'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
