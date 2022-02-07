# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='matrixdisplay',
    version='0.1.0',
    description='Display for the ClassicDIY using RGB LED Matrix Display',
    long_description=readme,
    author='Matt Sargent',
    author_email='matthew.c.sargent@gmail.com',
    url='https://github.com/mcsarge/ClassicDIY_MatrixDisplay',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

