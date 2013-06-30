#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name = "astro",
    version = "0.1-dev",
    license = "WTFPL",
    url = "http://github.com/buckket/astro",

    author = "buckket",
    author_email = "buckket@devnull",

    description = "Extensible daemon controlling a BeagleBone and attached devices",
    long_description=__doc__,

    scripts = ['bin/astro'],
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,

    install_requires=[
        'requests',
        'msgpack-python',
    ],
)
