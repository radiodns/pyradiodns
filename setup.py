from setuptools import setup
setup(name='pyradiodns',
      version='0.1',
      description='A Python port of phpradiodns.',
      author='samstarling',
      url='http://github.com/radiodns/pyradiodns',
      packages=['pyradiodns', 'pyradiodns.radiodns'],
      if sys.version_info[0] < 3:
          install_requires = ["dnspython<2.0"]
      else:
          install_requires = ["dnspython>=2.0"]
