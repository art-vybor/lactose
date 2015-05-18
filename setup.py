from setuptools import setup, find_packages

setup(name='lactose',
      packages=find_packages(),
      entry_points = {
        'console_scripts': [
            'lactose = lactose.translator:main',
        ]
      },
      install_requires=['antlr4-python2-runtime'],
      zip_safe=False)