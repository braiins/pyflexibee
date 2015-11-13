# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='pyflexibee',

    version='15.11',

    description='Python wrapper for accessing flexibee via REST API',
    long_description=long_description,

    url='http://github.com/braiins/pyflexibee',

    author='Jan Čapek',
    author_email='jan.capek@braiins.cz',

    # Choose your license
    license='GPL',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial :: Accounting'

        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python :: 2.7',
    ],
    # What does your project relate to?
    keywords='flexibee',

    packages=find_packages(),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['requests'],
)
