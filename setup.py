from setuptools import setup
setup(name='pyradiodns',
      version='0.1',
      description='A Python port of phpradiodns.',
      author='samstarling',
      url='http://github.com/radiodns/pyradiodns',
      packages=['pyradiodns', 'pyradiodns.radiodns'],
      install_requires=['dnspython'])
