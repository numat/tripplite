"""Package manager setup for TrippLite driver."""
from setuptools import setup

setup(
    name="tripplite",
    version="0.2.0",
    description="Python driver for TrippLite UPS battery backups.",
    url="http://github.com/numat/tripplite/",
    author="Patrick Fuller",
    author_email="pat@numat-tech.com",
    packages=['tripplite'],
    install_requires=['hidapi'],
    entry_points={
        'console_scripts': [('tripplite = tripplite:command_line')]
    },
    license='GPLv2',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces'
    ]
)
