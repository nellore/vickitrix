from setuptools import setup

setup(name='vickitrix',
      version='0.1.0',
      description='trade crypto on GDAX based on tweets',
      url='http://github.com/nellore/vickitrix',
      author='Abhi Nellore',
      author_email='anellore@gmail.com',
      license='MIT',
      packages=['vickitrix'],
      package_data={'vickitrix': ['*', './rules/*']},
      zip_safe=True,
      entry_points={
        'console_scripts': [
            'vickitrix=vickitrix:go',
        ],
    })
