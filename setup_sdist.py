'''
Setup.py only for creating a source distributions.

This file holds all the common setup.py keyword arguments between the source
distribution and the ordinary setup.py for binary distribution. Running this
instead of the default setup.py will create a GitHub-like archive with setup.py
meant for installing via pip.
'''

# pylint: disable=import-error,no-name-in-module
from distutils.core import setup
from os.path import join


with open(join('jnius', '__init__.py')) as fd:
    VERSION = [
        x for x in fd.readlines()
        if x.startswith('__version__')
    ][0].split("'")[-2]


SETUP_KWARGS = {
    'name': 'pyjnius',
    'version': VERSION,
    'packages': ['jnius'],
    'py_modules': ['jnius_config', 'setup'],
    'ext_package': 'jnius',
    'package_data': {
        'jnius': ['src/org/jnius/*'],
    },
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ]
}

if __name__ == '__main__':
    setup(**SETUP_KWARGS)
