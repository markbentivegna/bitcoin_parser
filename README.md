# bitcoin_parser

This Python module contains the Bitcoin parser described in BitcoinGraph. This scrapes the entire Bitcoin blockchain and memory pool. 

# Background

This project contains all of the Bitcoin parsing capabilities described in detail in the BitcoinGraph white paper. This is the most comprehensive and robust open-sourced Python solution for scraping the entire Bitcoin blockchain, including the memory pool. 

# Features

* Scrape entire Bitcoin blockchain 
* Parse memory pool and all pre-validated transactions for real-time insights
* Decode Bitcoin Script language to read locking and unlocking scripts
* Parallel read buffers for optimal performance
* Unit test cases with over 95% code coverage
* Regression tests that encapsulate all edge cases of the blockchain
* Comprehensive documentation included in BitcoinGraph white paper

# Installation

```
pip install blockchain_parser
```

# Testing

All unit tests targeting specific objects are contained in the `test/unit` directory. 

Regression test cases are much more thorough and comprehensive and scrape various portions of the blockchain to ensure that code changes don't break anything.

```
pytest
```
# Development

This project currently supports Python 3.8-3.10. Contributions are welcome!

```
git clone https://github.com/markbentivegna/bitcoin_parser.git
virtualenv -p python .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```


# Examples

See blockchain_parser.py for examples

# License

