from setuptools import setup

# required to suppress unwanted logs from
# the nose plugin manager in the SONiC build environment
import logging

logging.basicConfig()

setup()
