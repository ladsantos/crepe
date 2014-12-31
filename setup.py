try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'CREPE: CRoss-Entropy Parameter Estimation',
    'author': 'Leonardo dos Santos',
    'url': 'http://leosantos.org',
    'download_url': 'https://github.com/laugustogs/CREPE',
    'author_email': 'me@leosantos.org',
    'version': '0.1',
    'install_requires': ['nose','numpy','scipy'],
    'packages': ['crepe'],
    'name': 'crepe'
}

setup(**config)