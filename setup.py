"""setup.py for Bitcoin blockchain parser. For more details please see BitcoinGraph white paper"""
import setuptools
from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='BlockchainParser',
      version='1.0',
      description='Python package to scrape the Bitcoin blockchain',
      author='Mark Bentivegna',
      author_email='markbentivegna@gmail.com',
      long_description_content_type="text/markdown",
      url="https://github.com/markbentivegna/bitcoin_parser",
      include_package_data=True,
      packages=setuptools.find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      )
