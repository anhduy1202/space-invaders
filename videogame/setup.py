# Daniel Truong
# CPSC 386-02
# 2022-04-26
# anhduy1202@csu.fullerton.edu
# @anhduy1202
#
# Lab 05-00
#
# This is the steup file
#
""" Simple setup.py """

from setuptools import setup

setup_info = {
    "name": "videogame",
    "version": "0.1",
    "description": "A package to support writing games with PyGame",
    # TODO: Optional, add more information to the setup.py script
    # "long_description": open("README.md").read(),
    # "author": "Tuffy Titan",
    # "author_email": "tuffy@csu.fullerton.edu",
    # "url": "https://some.url/somehwere/maybe/github",
}

setup(**setup_info)
