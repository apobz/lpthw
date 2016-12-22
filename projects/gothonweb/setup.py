try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Gothons from Planet Percal #2: The Game',
    'author': 'apobz',
    'url': 'URL to get it at.'
    'download_url': 'Where to download it.',
    'author_email': 'anipobbati@gmailcom',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'gothonweb'
}


setup(**config)
