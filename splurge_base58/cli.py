#!/usr/bin/env python3
"""
Command-line interface for base-58 encoding and decoding operations.

This module provides a CLI for encoding binary data to base-58 strings
and decoding base-58 strings back to binary data.
"""

import sys
from typing import NoReturn

from splurge_base58.base58 import Base58, Base58Error


_MAX_ENCODE_INPUT_LENGTH = 2048


def _get_max_decode_input_length() -> int:
    """
    Calculate the maximum decode input length based on the maximum encode input length.
    
    This is calculated lazily to avoid circular dependencies during module import.
    
    Returns:
        Maximum length for decode input in characters
    """
    return len(Base58.encode(b'a' * _MAX_ENCODE_INPUT_LENGTH))


def print_usage() -> None:
    """Print usage information for the CLI."""
    print("Usage:")
    print("  python -m splurge_base58 encode <INPUT>")
    print("  python -m splurge_base58 decode <INPUT>")
    print()
    print("Commands:")
    print("  encode    Encode binary data to base-58 string")
    print("  decode    Decode base-58 string to binary data")
    print()
    print("Constraints:")
    print(f"  encode: max input length is {_MAX_ENCODE_INPUT_LENGTH} bytes")
    print(f"  decode: max input length is {_get_max_decode_input_length()} characters")


def encode_command(input_data: str) -> None:
    """
    Handle the encode command.
    
    Args:
        input_data: String input to encode (will be converted to bytes)
        
    Raises:
        SystemExit: If input is too long or encoding fails
    """
    if len(input_data) > _MAX_ENCODE_INPUT_LENGTH:
        print(f"Error: Input length {len(input_data)} exceeds maximum of {_MAX_ENCODE_INPUT_LENGTH}")
        sys.exit(1)
    
    try:
        # Convert string input to bytes
        data = input_data.encode('utf-8')
        encoded = Base58.encode(data)
        print(encoded)
    except UnicodeEncodeError as e:
        print(f"Error: Cannot encode input as UTF-8: {e}")
        sys.exit(1)
    except Base58Error as e:
        print(f"Error: {e}")
        sys.exit(1)


def decode_command(input_data: str) -> None:
    """
    Handle the decode command.
    
    Args:
        input_data: Base-58 string to decode
        
    Raises:
        SystemExit: If input is too long or decoding fails
    """
    max_decode_length = _get_max_decode_input_length()
    if len(input_data) > max_decode_length:
        print(f"Error: Input length {len(input_data)} exceeds maximum of {max_decode_length}")
        sys.exit(1)
    
    try:
        decoded = Base58.decode(input_data)
        # Convert bytes back to string for display
        result = decoded.decode('utf-8')
        print(result)
    except Base58Error as e:
        print(f"Error: {e}")
        sys.exit(1)
    except UnicodeDecodeError:
        print("Error: Decoded data is not valid UTF-8")
        sys.exit(1)
    except UnicodeEncodeError:
        # Handle case where console can't display the decoded text
        print("Error: Cannot display decoded data in current console encoding")
        sys.exit(1)


def main() -> NoReturn:
    """
    Main CLI entry point.
    
    Raises:
        SystemExit: Always exits with appropriate status code
    """
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    input_data = sys.argv[2]
    
    if command == "encode":
        encode_command(input_data)
    elif command == "decode":
        decode_command(input_data)
    else:
        print(f"Error: Unknown command '{command}'")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
