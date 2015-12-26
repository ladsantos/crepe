try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'CREPE: CRoss-Entropy Parameter Estimation',
    'author': 'Leonardo dos Santos',
    'download_url': 'https://github.com/laugustogs/CREPE',
    'author_email': 'leonardoags@usp.br',
    'version': '0.1.151226',
    'install_requires': ['numpy'],
    'packages': ['crepe'],
    'name': 'crepe'
}

setup(**config)
