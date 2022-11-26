from distutils.core import setup
import setuptools

setup(name='gfb-kafka-tools',
      version='1.0',
      description='GFB Kafka Tools',
      author='GFB',
      author_email='go.for.broke1006@python.net',
      url='https://none/',
      packages=[],
      install_requires=['setuptools', 'kafka-python==2.0.2'],
      scripts=['./kafka_kowalski.py'],
      entry_points={'console_scripts': ['kafwalski=kafka_kowalski:main']},
      )
