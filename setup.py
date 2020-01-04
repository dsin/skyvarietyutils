from setuptools import setup

setup(
    name='skyvarietyutils',
    version='0.0.1',
    description='My private package from private github repo',
    url='git@github.com:dsin/skyvarietyutils.git',
    author='dsin',
    author_email='dsin@skyvariety.com',
    install_requires=[
      'ply==3.11'
    ],
    license='unlicense',
    packages=['skyvarietyutils'],
    zip_safe=False
)
