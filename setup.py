from setuptools import setup

try:
    long_description=open('README.md', 'r').read()
except:
    long_description=''

setup(
    name='headlessxi',
    version='0.1',
    description='A headless client for DSP/TPZ/LSB-based servers.',
    long_description=long_description,
    url='https://github.com/zach2good/HeadlessXI',
    author='Zach Toogood (zach2good)',
    author_email='zrtoogood@gmail.com',
    license='GPLv3',
    packages=['headlessxi'])
