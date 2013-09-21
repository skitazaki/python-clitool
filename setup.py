from setuptools import setup

import clitool


setup(name='clitool',
      version=clitool.__version__,
      description="Command Line Tool Utilities",
      long_description=clitool.__doc__,
      classifiers=[ # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education"
      ],
      keywords='',
      author='KITAZAKI Shigeru',
      author_email='skitazaki@gmail.com',
      url='https://github.com/skitazaki/python-clitool',
      license='Apache',
      packages=['clitool'],
      package_dir={'clitool': 'clitool'},
      include_package_data=False,
      zip_safe=False,
      install_requires=[
        'six'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
