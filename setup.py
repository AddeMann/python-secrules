import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "requirements.txt")) as f:
    install_requires = f.readlines()
    
setup(
    name='python-secrules',
    version='1.0',
    packages=find_packages(),
    install_requires=install_requires
)
