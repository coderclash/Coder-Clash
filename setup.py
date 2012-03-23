from setuptools import setup, find_packages

VERSION = ("0", "0", "1")

setup(
    name='coderclash',
    version='.'.join(VERSION),
    description=(""),
    author='Bryan Helmig & Greg Aker',
    author_email='',
    url='https://github.com/coderclash/Coder-Clash',
    packages=find_packages(),
    package_data={'coderclash': ['bin/*.*', 'static/*.*', 'templates/*.*']},
    exclude_package_data={'coderclash': ['bin/*.pyc']},
    scripts=['coderclash/bin/app.py'],
)
