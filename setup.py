"""Package manager setup for TrippLite driver."""
from setuptools import setup

with open('README.md') as in_file:
    long_description = in_file.read()

setup(
    name="tripplite",
    version="0.4.0",
    description="Python driver for TrippLite UPS battery backups.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/numat/tripplite/",
    author="Patrick Fuller",
    author_email="pat@numat-tech.com",
    packages=['tripplite'],
    install_requires=['hidapi'],
    entry_points={
        'console_scripts': [
            'tripplite = tripplite:command_line',
        ],
    },
    extras_require={
        'exporter': ['prometheus_client'],
        'test': [
            'ruff',
        ],
    },
    license='GPLv2',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces'
    ]
)
