from setuptools import setup, find_packages

setup(
    name='VRGaze',
    version='1.0.0',
    url='https://github.com/vrijeuniversiteit/vrgaze.git',
    author='Daniel Müller',
    author_email='d.muller at vu.nl',
    description='Analysis pipelines for virtual reality experiments',
    packages=find_packages(),
    install_requires=['matplotlib >= 3.6.2'],
)