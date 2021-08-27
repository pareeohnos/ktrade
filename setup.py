# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

requires = [
    'flask==2.0.1',
    'flask-cors==3.0.10',
    'sqlalchemy==1.4',
    'Flask-SQLAlchemy==2.5',
    'Flask-Migrate==3.1.0',
    'sqlalchemy-utils==0.37.8',
    'ibapi==9.81.1.post1',
    'marshmallow==3.13'
]

setup(
    name='ktrade',
    version='0.0.1',
    description='A small utility for entering trades',
    long_description=readme,
    author='Adrian Hooper',
    author_email='ktrade@ca.hooper.co.uk,
    url='https://github.com/pareeohnos/ktrade',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=requires
)
