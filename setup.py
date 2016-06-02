from setuptools import setup, find_packages

setup(
  name = 'oz-python-client',
  packages = find_packages(),
  version = '0.6.0',
  description = 'A python client to the OZ API',
  install_requires = 'requests >= 2.8',
  author = 'Kari Tristan Helgason',
  author_email = 'kari@oz.com',
  url = 'https://github.com/ozinc/oz-python-client',
  keywords = ['oz', 'api-client', 'example'],
  classifiers = [],
)
