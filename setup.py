from setuptools import setup, find_packages

setup(name='afro',
      version='0.1',
      description='APFS file recovery',
      url='http://github.com/cugu/afro',
      author='Jonas Plum',
      license='GPL 3, MIT (see README.md)',
      packages=find_packages(),
      entry_points={
        'console_scripts': [
          'afro=afro:main',
        ],
      },
      install_requires=['kaitaistruct', 'colorlog']
)