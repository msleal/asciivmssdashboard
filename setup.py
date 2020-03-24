from setuptools import setup

setup(name='asciivmssdashboard',
      version='2.0',
      summary='Terminal Based Dashboard to show and configure Azure VM Scale Sets.',
      description='Terminal Based Dashboard to show and configure Azure VM Scale Sets.',
      url='http://github.com/msleal/asciivmssdashboard',
      author='msleal',
      author_email='msl@eall.com.br',
      license='MIT',
      packages=['asciivmssdashboard'],
      install_requires=[
          'azurerm',
          'requests',
      ],
      zip_safe=False)
