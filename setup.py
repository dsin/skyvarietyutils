from setuptools import setup

setup(
    name='skyvarietyutils',
    version='0.0.2',
    description='My private package from private github repo',
    url='git@github.com:dsin/skyvarietyutils.git',
    author='dsin',
    author_email='dsin@skyvariety.com',
    install_requires=[
      'ply==3.11',
      'tweepy===3.8.0',
      'twitter-ads==6.1.0',
      # '-e git+ssh://git@github.com/michaelliao/sinaweibopy.git#egg=sinaweibopy',
    ],
    license='unlicense',
    packages=['skyvarietyutils'],
    zip_safe=False
)
