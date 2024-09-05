from setuptools import setup, find_packages

#Setup meta data
setup(
    name="sonar_py_project",
    version="0.1",
    packages=find_packages(where='src'),
    package_dir={'':'src'},
    test_suite='tests',
    install_requires=['coverage',],
)