import setuptools

setuptools.setup(
    name='skyvarietyutils',
    version='0.0.1',
    description='My private package from private github repo',
    url='git@github.com:dsin/skyvarietyutils.git',
    author='dsin',
    author_email='dsin@skyvariety.com',
    install_requires=[
      'ply==3.11',
      'six',
      #'tweepy===3.8.0',
      'twitter-ads==6.1.0',
      'twitter',
      # '-e git+ssh://git@github.com/michaelliao/sinaweibopy.git#egg=sinaweibopy',
      'facebook-sdk',
      'algoliasearch>=2.0,<3.0'
    ],
    license='proprietary',
    packages=setuptools.find_packages(),
    package_dir={'skyvarietyutils': 'skyvarietyutils'},
    zip_safe=False
)
