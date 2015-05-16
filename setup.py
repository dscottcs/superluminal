import setuptools

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='superluminal',
    version='0.0.2',

    description='Ansible communication for humans',

    # Author details
    author='David Scott',
    author_email='david.scott@emc.com',

    # Choose your license
    license='Apache v2',

    packages=['superluminal'],
    include_package_data=True,

    install_requires=[
        'gunicorn',
        'oslo.config',
        'falcon'
    ],

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[('my_data', ['data/data_file'])],
)
