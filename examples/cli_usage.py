#!/usr/bin/env python3
"""
CLI End-to-End Workflow Example for splurge_base58.

This example demonstrates how to use the splurge_base58 CLI commands
for encoding and decoding data. It shows the complete workflow from
input to output and back.
"""

import subprocess
import sys
from typing import Tuple


def run_cli_command(command: str, input_data: str) -> Tuple[int, str, str]:
    """
    Run a splurge_base58 CLI command and capture the output.
    
    Args:
        command: The CLI command to run ('encode' or 'decode')
        input_data: The input data for the command
        
    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'splurge_base58', command, input_data],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"
    except Exception as e:
        return 1, "", str(e)


def demonstrate_encode_workflow() -> None:
    """Demonstrate the encode workflow."""
    print("=== ENCODE WORKFLOW ===")
    
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
        
        # Encode the string
        return_code, stdout, stderr = run_cli_command('encode', test_string)
        
        if return_code == 0:
            encoded = stdout
            print(f"Encoded: {encoded}")
            
            # Decode back to verify
            return_code, decoded, stderr = run_cli_command('decode', encoded)
            
            if return_code == 0:
                print(f"Decoded: '{decoded}'")
                if decoded == test_string:
                    print("✓ Round-trip successful")
                else:
                    print("✗ Round-trip failed")
            else:
                print(f"✗ Decode failed: {stderr}")
        else:
            print(f"✗ Encode failed: {stderr}")


def demonstrate_decode_workflow() -> None:
    """Demonstrate the decode workflow."""
    print("\n=== DECODE WORKFLOW ===")
    
    # Test with known base58 strings
    test_encodings = [
        "JxF12TrwUP45BMd",  # "Hello"
        "2NEpo7TZRRrLZSi2U",  # "World"
        "11111111111111111111111111111111",  # All zeros
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"  # Bitcoin address format
    ]
    
    for encoded in test_encodings:
        print(f"\nEncoded: {encoded}")
        
        # Decode the string
        return_code, stdout, stderr = run_cli_command('decode', encoded)
        
        if return_code == 0:
            decoded = stdout
            print(f"Decoded: '{decoded}'")
        else:
            print(f"✗ Decode failed: {stderr}")


def demonstrate_error_handling() -> None:
    """Demonstrate error handling scenarios."""
    print("\n=== ERROR HANDLING ===")
    
    # Test invalid base58 string
    print("\nTesting invalid base58 string:")
    return_code, stdout, stderr = run_cli_command('decode', 'invalid!@#')
    print(f"Input: 'invalid!@#'")
    print(f"Return code: {return_code}")
    print(f"Error: {stderr}")
    
    # Test empty input
    print("\nTesting empty input:")
    return_code, stdout, stderr = run_cli_command('encode', '')
    print(f"Input: ''")
    print(f"Return code: {return_code}")
    print(f"Error: {stderr}")
    
    # Test unknown command
    print("\nTesting unknown command:")
    return_code, stdout, stderr = run_cli_command('invalid', 'test')
    print(f"Command: 'invalid'")
    print(f"Return code: {return_code}")
    print(f"Error: {stderr}")


def demonstrate_length_constraints() -> None:
    """Demonstrate input length constraints."""
    print("\n=== LENGTH CONSTRAINTS ===")
    
    # Test maximum encode length
    max_length_string = "a" * 2048
    print(f"\nTesting maximum encode length ({len(max_length_string)} characters):")
    return_code, stdout, stderr = run_cli_command('encode', max_length_string)
    
    if return_code == 0:
        print("✓ Maximum length encode successful")
        encoded = stdout
        print(f"Encoded length: {len(encoded)} characters")
        
        # Test decode of maximum length
        return_code, decoded, stderr = run_cli_command('decode', encoded)
        if return_code == 0:
            print("✓ Maximum length decode successful")
        else:
            print(f"✗ Maximum length decode failed: {stderr}")
    else:
        print(f"✗ Maximum length encode failed: {stderr}")
    
    # Test exceeding maximum encode length
    too_long_string = "a" * 2049
    print(f"\nTesting exceeding maximum encode length ({len(too_long_string)} characters):")
    return_code, stdout, stderr = run_cli_command('encode', too_long_string)
    print(f"Return code: {return_code}")
    print(f"Error: {stderr}")


def main() -> None:
    """Main function to run all demonstrations."""
    print("splurge_base58 CLI End-to-End Workflow Examples")
    print("=" * 50)
    
    try:
        demonstrate_encode_workflow()
        demonstrate_decode_workflow()
        demonstrate_error_handling()
        demonstrate_length_constraints()
        
        print("\n" + "=" * 50)
        print("All demonstrations completed!")
        
    except KeyboardInterrupt:
        print("\n\nDemonstration interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
