from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ["tensorflow==1.5", "numpy==1.14.1"]

setup(
    name='trainer',
    version='0.5',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='My trainer application package.'
)
