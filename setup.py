import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="launch_on_workspace",
    version="1.0.0",
    description="Launch applications on a given workspace and given monitor in Linux",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/xblahoud/launch_on_workspace",
    author="Fanda Blahoudek",
    author_email="fandikb+low@gmail.com",
    license="MIT",
    python_requires=">=3.6.0",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["launch_on_workspace"],
)
