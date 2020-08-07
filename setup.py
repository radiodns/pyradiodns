from setuptools import setup
if sys.version_info[0] < 3:
      install_requires = ["dnspython<2.0"]
else:
      install_requires = ["dnspython>=2.0"]
      
setup(name='pyradiodns',
      version='0.1',
      description='A Python port of phpradiodns.',
      author='samstarling',
      url='http://github.com/radiodns/pyradiodns',
      packages=['pyradiodns', 'pyradiodns.radiodns'],
      install_requires=install_requires)
