"""
Sanic
"""
import codecs
import os
import re
import sys
from distutils.util import strtobool

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    """
    Provide a Test runner to be used from setup.py to run unit tests
    """

    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        import shlex
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


def open_local(paths, mode="r", encoding="utf8"):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), *paths)

    return codecs.open(path, mode, encoding)


with open_local(["sanic", "__init__.py"], encoding="latin1") as fp:
    try:
        version = re.findall(
            r"^__version__ = \"([^']+)\"\r?$", fp.read(), re.M
        )[0]
    except IndexError:
        raise RuntimeError("Unable to determine version.")

with open_local(["README.rst"]) as rm:
    long_description = rm.read()

setup_kwargs = {
    "name": "sanic",
    "version": version,
    "url": "http://github.com/huge-success/sanic/",
    "license": "MIT",
    "author": "Sanic Community",
    "author_email": "admhpkns@gmail.com",
    "description": (
        "A web server and web framework that's written to go fast. Build fast. Run fast."
    ),
    "long_description": long_description,
    "packages": ["sanic"],
    "platforms": "any",
    "classifiers": [
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
}

env_dependency = (
    '; sys_platform != "win32" ' 'and implementation_name == "cpython"'
)
ujson = "ujson>=1.35" + env_dependency
uvloop = "uvloop>=0.5.3" + env_dependency

requirements = [
    "httptools>=0.0.10",
    uvloop,
    ujson,
    "aiofiles>=0.3.0",
    "websockets>=6.0",
    "multidict>=4.0,<5.0",
    "requests-async==0.5.0",
]

tests_require = [
    "pytest==4.1.0",
    "multidict>=4.0,<5.0",
    "gunicorn",
    "pytest-cov",
    "httpcore==0.3.0",
    "beautifulsoup4",
    uvloop,
    ujson,
    "pytest-sanic",
    "pytest-sugar",
    "pytest-benchmark",
]

if strtobool(os.environ.get("SANIC_NO_UJSON", "no")):
    print("Installing without uJSON")
    requirements.remove(ujson)
    tests_require.remove(ujson)

# 'nt' means windows OS
if strtobool(os.environ.get("SANIC_NO_UVLOOP", "no")):
    print("Installing without uvLoop")
    requirements.remove(uvloop)
    tests_require.remove(uvloop)

extras_require = {
    "test": tests_require,
    "dev": tests_require + ["aiofiles", "tox", "black", "flake8", "bandit"],
    "docs": [
        "sphinx",
        "sphinx_rtd_theme",
        "recommonmark",
        "sphinxcontrib-asyncio",
        "docutils",
        "pygments",
    ],
}

setup_kwargs["install_requires"] = requirements
setup_kwargs["tests_require"] = tests_require
setup_kwargs["extras_require"] = extras_require
setup_kwargs["cmdclass"] = {"test": PyTest}
setup(**setup_kwargs)
