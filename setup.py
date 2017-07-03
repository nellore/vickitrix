from setuptools import setup

setup(name='vickitrix',
      version='0.1.0',
      description='trade crypto on GDAX based on tweets',
      url='http://github.com/nellore/vickitrix',
      download_url = 'https://github.com/nellore/vickitrix/tarball/0.1.0',
      author='Abhi Nellore',
      author_email='anellore@gmail.com',
      license='MIT',
      packages=['vickitrix'],
      package_data={'vickitrix': ['*.py', './rules/*']},
      zip_safe=True,
      install_requires=[
      		'tweepy', 'gdax', 'pycrypto'
      	],
      entry_points={
        'console_scripts': [
            'vickitrix=vickitrix:go',
        ],},
      keywords=['bitcoin', 'btc', 'ethereum', 'eth', 'twitter'],
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Operating System :: MacOS',
          'Operating System :: Unix',
          'Topic :: Utilities'
        ]
    )
