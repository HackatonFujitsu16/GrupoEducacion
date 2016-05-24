from setuptools import setup
from lod4all import __version__

setup(
    name             = 'py-lod4all',
    version          = __version__,
    description      = 'Python library for LOD4ALL',
    url              = 'http://lod4all.net/',
    author           = 'Fujitsu Laboratories of Europe',
    author_email     = 'lod4all-contact@ml.labs.fujitsu.com',
    license          = 'TODO update licese',
    packages         = ['lod4all'],
    zip_safe         = True,
    install_requires = [
        # Included in Python 2 standard libs
        #'httplib',
        #'urllib',
        #'json',
    ],
    extras_require   = {
        'Testing with test.py': ['nose']
    },
)
