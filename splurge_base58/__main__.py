"""
Entry point for running splurge_base58 as a module.

This allows the package to be run as:
    python -m splurge_base58 encode <input>
    python -m splurge_base58 decode <input>
"""

from splurge_base58.cli import main

if __name__ == "__main__":
    main()
