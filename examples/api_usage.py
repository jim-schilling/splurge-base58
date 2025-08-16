#!/usr/bin/env python3
"""
API End-to-End Workflow Example for splurge_base58.

This example demonstrates how to use the splurge_base58 Base58 class
directly in Python code for encoding and decoding operations.
"""

import hashlib
import json
from typing import Any, Dict, List

from splurge_base58.base58 import Base58, Base58Error


def demonstrate_basic_encoding() -> None:
    """Demonstrate basic encoding operations."""
    print("=== BASIC ENCODING ===")
    
    # Test data
    test_strings = [
        "Hello, World!",
        "Base58 encoding example",
        "1234567890",
        "Special chars: !@#$%^&*()",
        "Unicode: 你好世界 🌍"
    ]
    
    for test_string in test_strings:
        print(f"\nInput: '{test_string}'")
        
        try:
            # Convert string to bytes and encode
            data = test_string.encode('utf-8')
            encoded = Base58.encode(data)
            print(f"Encoded: {encoded}")
            
            # Decode back to verify
            decoded_bytes = Base58.decode(encoded)
            decoded_string = decoded_bytes.decode('utf-8')
            print(f"Decoded: '{decoded_string}'")
            
            if decoded_string == test_string:
                print("✓ Round-trip successful")
            else:
                print("✗ Round-trip failed")
                
        except Base58Error as e:
            print(f"✗ Error: {e}")
        except UnicodeDecodeError as e:
            print(f"✗ Unicode decode error: {e}")


def demonstrate_binary_data_encoding() -> None:
    """Demonstrate encoding of binary data."""
    print("\n=== BINARY DATA ENCODING ===")
    
    # Test with various binary data
    test_cases = [
        (b'\x00\x01\x02\x03', "Zero-prefixed bytes"),
        (b'\xff\xfe\xfd\xfc', "High-value bytes"),
        (b'\x00\x00\x00\x00', "All zeros"),
        (b'\xff\xff\xff\xff', "All ones"),
        (hashlib.sha256(b"test").digest(), "SHA256 hash"),
        (b'\x00' * 10, "Multiple leading zeros"),
    ]
    
    for binary_data, description in test_cases:
        print(f"\n{description}: {binary_data.hex()}")
        
        try:
            encoded = Base58.encode(binary_data)
            print(f"Encoded: {encoded}")
            
            decoded = Base58.decode(encoded)
            print(f"Decoded: {decoded.hex()}")
            
            if decoded == binary_data:
                print("✓ Round-trip successful")
            else:
                print("✗ Round-trip failed")
                
        except Base58Error as e:
            print(f"✗ Error: {e}")


def demonstrate_validation() -> None:
    """Demonstrate validation functionality."""
    print("\n=== VALIDATION ===")
    
    # Test valid and invalid base58 strings
    test_strings = [
        ("JxF12TrwUP45BMd", "Valid base58"),
        ("invalid!@#", "Invalid characters"),
        ("", "Empty string"),
        ("11111111111111111111111111111111", "All ones"),
        ("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "Bitcoin address format"),
        ("0OlI", "Contains zero and O"),
    ]
    
    for test_string, description in test_strings:
        print(f"\n{description}: '{test_string}'")
        
        is_valid = Base58.is_valid(test_string)
        print(f"Valid: {is_valid}")
        
        if is_valid:
            try:
                decoded = Base58.decode(test_string)
                print(f"Decoded: {decoded.hex()}")
            except Base58Error as e:
                print(f"✗ Decode error: {e}")
        else:
            try:
                decoded = Base58.decode(test_string)
                print(f"Unexpectedly decoded: {decoded.hex()}")
            except Base58Error as e:
                print(f"✓ Correctly rejected: {e}")


def demonstrate_error_handling() -> None:
    """Demonstrate error handling scenarios."""
    print("\n=== ERROR HANDLING ===")
    
    # Test various error conditions
    error_cases = [
        (123, "Integer input for encode", "encode"),
        (b"", "Empty bytes for encode", "encode"),
        ("invalid!@#", "Invalid base58 for decode", "decode"),
        ("", "Empty string for decode", "decode"),
        (None, "None input for encode", "encode"),
    ]
    
    for test_input, description, operation in error_cases:
        print(f"\n{description}: {test_input}")
        
        try:
            if operation == "encode":
                if isinstance(test_input, bytes):
                    result = Base58.encode(test_input)
                elif test_input is None:
                    result = Base58.encode(b'')
                else:
                    result = Base58.encode(test_input.encode('utf-8'))
                print(f"Encoded: {result}")
            else:  # decode
                result = Base58.decode(test_input)
                print(f"Decoded: {result.hex()}")
                
        except Base58Error as e:
            print(f"✓ Caught Base58Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {type(e).__name__}: {e}")


def demonstrate_length_constraints() -> None:
    """Demonstrate input length constraints."""
    print("\n=== LENGTH CONSTRAINTS ===")
    
    # Test maximum encode length
    max_length_data = b'a' * 2048
    print(f"\nTesting maximum encode length ({len(max_length_data)} bytes):")
    
    try:
        encoded = Base58.encode(max_length_data)
        print(f"✓ Maximum length encode successful")
        print(f"Encoded length: {len(encoded)} characters")
        
        decoded = Base58.decode(encoded)
        if decoded == max_length_data:
            print("✓ Maximum length round-trip successful")
        else:
            print("✗ Maximum length round-trip failed")
            
    except Base58Error as e:
        print(f"✗ Maximum length encode failed: {e}")
    
    # Test exceeding maximum encode length
    too_long_data = b'a' * 2049
    print(f"\nTesting exceeding maximum encode length ({len(too_long_data)} bytes):")
    
    try:
        encoded = Base58.encode(too_long_data)
        print(f"Encoded: {encoded}")
    except Base58Error as e:
        print(f"✓ Correctly rejected: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


def demonstrate_practical_examples() -> None:
    """Demonstrate practical use cases."""
    print("\n=== PRACTICAL EXAMPLES ===")
    
    # Example 1: Encoding a JSON payload
    print("\n1. Encoding JSON payload:")
    json_data = {
        "user_id": 12345,
        "timestamp": "2024-01-15T10:30:00Z",
        "action": "login"
    }
    
    json_string = json.dumps(json_data)
    json_bytes = json_string.encode('utf-8')
    
    try:
        encoded = Base58.encode(json_bytes)
        print(f"JSON: {json_string}")
        print(f"Encoded: {encoded}")
        
        decoded = Base58.decode(encoded)
        decoded_json = decoded.decode('utf-8')
        print(f"Decoded JSON: {decoded_json}")
        
        if decoded_json == json_string:
            print("✓ JSON round-trip successful")
            
    except Base58Error as e:
        print(f"✗ Error: {e}")
    
    # Example 2: Encoding binary file data
    print("\n2. Encoding binary file data:")
    file_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
    
    try:
        encoded = Base58.encode(file_data)
        print(f"File header: {file_data.hex()}")
        print(f"Encoded: {encoded}")
        
        decoded = Base58.decode(encoded)
        print(f"Decoded: {decoded.hex()}")
        
        if decoded == file_data:
            print("✓ File data round-trip successful")
            
    except Base58Error as e:
        print(f"✗ Error: {e}")
    
    # Example 3: Encoding hash values
    print("\n3. Encoding hash values:")
    hash_data = hashlib.sha256(b"password123").digest()
    
    try:
        encoded = Base58.encode(hash_data)
        print(f"Hash: {hash_data.hex()}")
        print(f"Encoded: {encoded}")
        
        decoded = Base58.decode(encoded)
        print(f"Decoded: {decoded.hex()}")
        
        if decoded == hash_data:
            print("✓ Hash round-trip successful")
            
    except Base58Error as e:
        print(f"✗ Error: {e}")


def demonstrate_performance_comparison() -> None:
    """Demonstrate performance characteristics."""
    print("\n=== PERFORMANCE COMPARISON ===")
    
    import time
    
    # Test different data sizes
    test_sizes = [10, 100, 1000, 2048]
    
    for size in test_sizes:
        data = b'a' * size
        print(f"\nTesting {size} bytes:")
        
        # Time encoding
        start_time = time.time()
        try:
            encoded = Base58.encode(data)
            encode_time = time.time() - start_time
            
            # Time decoding
            start_time = time.time()
            decoded = Base58.decode(encoded)
            decode_time = time.time() - start_time
            
            print(f"  Encode time: {encode_time:.6f}s")
            print(f"  Decode time: {decode_time:.6f}s")
            print(f"  Encoded length: {len(encoded)} characters")
            print(f"  Compression ratio: {len(encoded) / len(data):.2f}")
            
            if decoded == data:
                print("  ✓ Round-trip successful")
            else:
                print("  ✗ Round-trip failed")
                
        except Base58Error as e:
            print(f"  ✗ Error: {e}")


def main() -> None:
    """Main function to run all demonstrations."""
    print("splurge_base58 API End-to-End Workflow Examples")
    print("=" * 50)
    
    try:
        demonstrate_basic_encoding()
        demonstrate_binary_data_encoding()
        demonstrate_validation()
        demonstrate_error_handling()
        demonstrate_length_constraints()
        demonstrate_practical_examples()
        demonstrate_performance_comparison()
        
        print("\n" + "=" * 50)
        print("All demonstrations completed!")
        
    except KeyboardInterrupt:
        print("\n\nDemonstration interrupted by user.")
        return
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        return


if __name__ == "__main__":
    main()
