'''
Setup.py only for creating a source distributions.

This file holds all the common setup.py keyword arguments between the source
distribution and the ordinary setup.py for binary distribution. Running this
instead of the default setup.py will create a GitHub-like archive with setup.py
meant for installing via pip.
'''
from io import open

# pylint: disable=import-error,no-name-in-module
from setuptools import setup
from os.path import join

with open("README.md", encoding='utf8') as f:
    README = f.read()


with open(join('jnius', '__init__.py')) as fd:
    VERSION = [
        x for x in fd.readlines()
        if x.startswith('__version__')
    ][0].split("'")[-2]


SETUP_KWARGS = {
    'name': 'pyjnius',
    'version': VERSION,
    'url': "https://github.com/kivy/pyjnius",
    'packages': ['jnius'],
    'py_modules': ['jnius_config', 'setup', 'setup_sdist', 'jnius.env'],
    'ext_package': 'jnius',
    'package_data': {
        'jnius': ['src/org/jnius/*'],
    },
    'long_description_content_type': 'text/markdown',
    'long_description': README,
    'author': 'Kivy Team and other contributors',
    'author_email': 'kivy-dev@googlegroups.com',
    'description': "A Python module to access Java classes as Python classes using JNI.",
    'keywords': 'Java JNI Android',
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Android',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ]
}

if __name__ == '__main__':
    setup(**SETUP_KWARGS)
