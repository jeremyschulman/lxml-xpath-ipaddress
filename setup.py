from setuptools import setup, find_packages


def requirements(filename='requirements.txt'):
    return open(filename.strip()).readlines()


setup(
    name='lxml-ext-ipaddress',
    version='0.1.0',
    description='LXML extension library for ipaddress',
    author='jschulman@juniper.net',
    packages=find_packages(),
    install_requires=requirements()
)
