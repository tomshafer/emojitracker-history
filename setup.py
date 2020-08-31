"""Package setup script."""

import os

from setuptools import setup


def get_version():
    """Extract version number from emojihistory.py."""
    with open(os.path.join(os.path.dirname(__file__), "emojihistory.py")) as f:
        for line in map(lambda l: l.strip().split(), f):
            if line and "__version__" in line[0]:
                return line[-1].strip("'\"")


setup(
    name="emojihistory",
    version=get_version(),
    description="Poll the emojitracker to compile historical data",
    url="https://github.com/tomshafer/emojitracker-history",
    author="Tom Shafer",
    author_email="contact@tshafer.com",
    py_modules=["emojihistory"],
    install_requires=["requests"],
)
