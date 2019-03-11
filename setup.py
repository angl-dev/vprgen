import os
from setuptools import setup

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name = "vprgen",
        version = "0.0.1",
        author = "Ang Li",
        author_email = "angl@princeton.edu",
        description = "VPR's architecture description and routing resource graph XML generation API",
        url = "https://github.com/leon575777642/vprgen",
        packages = ["vprgen"],
        include_package_data = True,
        long_description = read("README.md"),
        classifiers = [
            "Development Status :: 1 - Planning",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.7",
            "Topic :: Utilities",
            ],
        install_requires = ["lxml", "jsonschema>=3.0.0", "future"],
        setup_requires = ["pytest-runner"],
        tests_require = ["pytest", "xmltodict"],
        )
