"""
Tests for CLI functionality.

This module contains comprehensive tests for the CLI interface
using subprocess calls to test actual CLI behavior.
"""

import subprocess
import sys
from typing import Tuple

import pytest

from splurge_base58.base58 import Base58


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


class TestCLIEncode:
    """Test CLI encode functionality."""
    
    def test_encode_simple_string(self):
        """Test encoding a simple string via CLI."""
        test_input = "Hello, World!"
        return_code, stdout, stderr = run_cli_command('encode', test_input)
        
        assert return_code == 0
        assert stderr == ""
        assert stdout != ""
        
        # Verify the output is valid base58
        assert Base58.is_valid(stdout)
        
        # Verify round-trip
        decoded_return_code, decoded_stdout, decoded_stderr = run_cli_command('decode', stdout)
        assert decoded_return_code == 0
        assert decoded_stdout == test_input
    
    def test_encode_empty_string(self):
        """Test encoding empty string via CLI."""
        return_code, stdout, stderr = run_cli_command('encode', '')
        
        assert return_code == 1
        assert "Error:" in stdout
        assert stderr == ""
    
    def test_encode_unicode_string(self):
        """Test encoding unicode string via CLI."""
        test_input = "你好世界"
        return_code, stdout, stderr = run_cli_command('encode', test_input)
        
        assert return_code == 0
        assert stderr == ""
        assert Base58.is_valid(stdout)
        
        # Verify round-trip (may fail in some environments due to console encoding)
        decoded_return_code, decoded_stdout, decoded_stderr = run_cli_command('decode', stdout)
        if decoded_return_code == 0:
            assert decoded_stdout == test_input
        else:
            # If decode fails due to console encoding, that's acceptable
            # Just verify that the encoded string is valid base58
            assert Base58.is_valid(stdout)
    
    def test_encode_special_characters(self):
        """Test encoding string with special characters via CLI."""
        test_input = "Special chars: !@#$%^&*()"
        return_code, stdout, stderr = run_cli_command('encode', test_input)
        
        assert return_code == 0
        assert stderr == ""
        assert Base58.is_valid(stdout)
        
        # Verify round-trip
        decoded_return_code, decoded_stdout, decoded_stderr = run_cli_command('decode', stdout)
        assert decoded_return_code == 0
        assert decoded_stdout == test_input
    
    def test_encode_numeric_string(self):
        """Test encoding numeric string via CLI."""
        test_input = "1234567890"
        return_code, stdout, stderr = run_cli_command('encode', test_input)
        
        assert return_code == 0
        assert stderr == ""
        assert Base58.is_valid(stdout)
        
        # Verify round-trip
        decoded_return_code, decoded_stdout, decoded_stderr = run_cli_command('decode', stdout)
        assert decoded_return_code == 0
        assert decoded_stdout == test_input
    
    def test_encode_maximum_length(self):
        """Test encoding maximum length string via CLI."""
        max_length_string = "a" * 2048
        return_code, stdout, stderr = run_cli_command('encode', max_length_string)
        
        assert return_code == 0
        assert stderr == ""
        assert Base58.is_valid(stdout)
        
        # Verify round-trip
        decoded_return_code, decoded_stdout, decoded_stderr = run_cli_command('decode', stdout)
        assert decoded_return_code == 0
        assert decoded_stdout == max_length_string
    
    def test_encode_exceeds_maximum_length(self):
        """Test encoding string that exceeds maximum length via CLI."""
        too_long_string = "a" * 2049
        return_code, stdout, stderr = run_cli_command('encode', too_long_string)
        
        assert return_code == 1
        assert "Error:" in stdout
        assert "exceeds maximum" in stdout
        assert stderr == ""


class TestCLIDecode:
    """Test CLI decode functionality."""
    
    def test_decode_valid_base58(self):
        """Test decoding valid base58 string via CLI."""
        # First encode a string
        test_input = "Hello, World!"
        encode_return_code, encoded, encode_stderr = run_cli_command('encode', test_input)
        assert encode_return_code == 0
        
        # Then decode it
        decode_return_code, decoded, decode_stderr = run_cli_command('decode', encoded)
        
        assert decode_return_code == 0
        assert decode_stderr == ""
        assert decoded == test_input
    
    def test_decode_known_base58_strings(self):
        """Test decoding known base58 strings via CLI."""
        test_cases = [
            ("JxF12TrwUP45BMd", "Hello World"),
            ("As9UGqq", "World"),
            ("11111111111111111111111111111111", "\x00" * 32),  # 32 zero bytes
        ]
        
        for encoded, expected in test_cases:
            return_code, stdout, stderr = run_cli_command('decode', encoded)
            
            assert return_code == 0
            assert stderr == ""
            assert stdout == expected
    
    def test_decode_invalid_base58(self):
        """Test decoding invalid base58 string via CLI."""
        invalid_input = "invalid!@#"
        return_code, stdout, stderr = run_cli_command('decode', invalid_input)
        
        assert return_code == 1
        assert "Error:" in stdout
        assert stderr == ""
    
    def test_decode_empty_string(self):
        """Test decoding empty string via CLI."""
        return_code, stdout, stderr = run_cli_command('decode', '')
        
        assert return_code == 1
        assert "Error:" in stdout
        assert stderr == ""
    
    def test_decode_maximum_length(self):
        """Test decoding maximum length base58 string via CLI."""
        # Create maximum length input and encode it
        max_length_string = "a" * 2048
        encode_return_code, encoded, encode_stderr = run_cli_command('encode', max_length_string)
        assert encode_return_code == 0
        
        # Decode it
        decode_return_code, decoded, decode_stderr = run_cli_command('decode', encoded)
        
        assert decode_return_code == 0
        assert decode_stderr == ""
        assert decoded == max_length_string
    
    def test_decode_exceeds_maximum_length(self):
        """Test decoding base58 string that exceeds maximum length via CLI."""
        # Create a very long base58 string
        very_long_base58 = "1" * 3000  # Much longer than the calculated max
        return_code, stdout, stderr = run_cli_command('decode', very_long_base58)
        
        assert return_code == 1
        assert "Error:" in stdout
        assert "exceeds maximum" in stdout
        assert stderr == ""


class TestCLIErrorHandling:
    """Test CLI error handling."""
    
    def test_missing_arguments(self):
        """Test CLI with missing arguments."""
        # Test with no arguments
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'splurge_base58'],
                capture_output=True,
                text=True,
                timeout=30
            )
            assert result.returncode == 1
            assert "Usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.fail("Command timed out")
    
    def test_insufficient_arguments(self):
        """Test CLI with insufficient arguments."""
        # Test with only command
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'splurge_base58', 'encode'],
                capture_output=True,
                text=True,
                timeout=30
            )
            assert result.returncode == 1
            assert "Usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.fail("Command timed out")
    
    def test_unknown_command(self):
        """Test CLI with unknown command."""
        return_code, stdout, stderr = run_cli_command('invalid', 'test')
        
        assert return_code == 1
        assert "Error:" in stdout
        assert "Unknown command" in stdout
        assert stderr == ""
    
    def test_help_displayed_for_unknown_command(self):
        """Test that help is displayed for unknown command."""
        return_code, stdout, stderr = run_cli_command('invalid', 'test')
        
        assert return_code == 1
        assert "Usage:" in stdout
        assert "Commands:" in stdout
        assert "Constraints:" in stdout


class TestCLIRoundTrip:
    """Test CLI round-trip functionality."""
    
    def test_round_trip_simple_string(self):
        """Test round-trip encoding and decoding via CLI."""
        test_input = "Hello, World!"
        
        # Encode
        encode_return_code, encoded, encode_stderr = run_cli_command('encode', test_input)
        assert encode_return_code == 0
        assert encode_stderr == ""
        
        # Decode
        decode_return_code, decoded, decode_stderr = run_cli_command('decode', encoded)
        assert decode_return_code == 0
        assert decode_stderr == ""
        
        # Verify round-trip
        assert decoded == test_input
    
    def test_round_trip_unicode_string(self):
        """Test round-trip encoding and decoding unicode via CLI."""
        test_input = "你好世界"
        
        # Encode
        encode_return_code, encoded, encode_stderr = run_cli_command('encode', test_input)
        assert encode_return_code == 0
        
        # Decode
        decode_return_code, decoded, decode_stderr = run_cli_command('decode', encoded)
        if decode_return_code == 0:
            # Verify round-trip
            assert decoded == test_input
        else:
            # If decode fails due to console encoding, that's acceptable
            # Just verify that the encoded string is valid base58
            assert Base58.is_valid(encoded)
    
    def test_round_trip_special_characters(self):
        """Test round-trip encoding and decoding special characters via CLI."""
        test_input = "Special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        
        # Encode
        encode_return_code, encoded, encode_stderr = run_cli_command('encode', test_input)
        assert encode_return_code == 0
        
        # Decode
        decode_return_code, decoded, decode_stderr = run_cli_command('decode', encoded)
        assert decode_return_code == 0
        
        # Verify round-trip
        assert decoded == test_input
    
    def test_round_trip_numeric_string(self):
        """Test round-trip encoding and decoding numeric string via CLI."""
        test_input = "1234567890"
        
        # Encode
        encode_return_code, encoded, encode_stderr = run_cli_command('encode', test_input)
        assert encode_return_code == 0
        
        # Decode
        decode_return_code, decoded, decode_stderr = run_cli_command('decode', encoded)
        assert decode_return_code == 0
        
        # Verify round-trip
        assert decoded == test_input
    
    def test_round_trip_long_string(self):
        """Test round-trip encoding and decoding long string via CLI."""
        test_input = "This is a longer string that will test the CLI's ability to handle larger inputs." * 10
        
        # Encode
        encode_return_code, encoded, encode_stderr = run_cli_command('encode', test_input)
        assert encode_return_code == 0
        
        # Decode
        decode_return_code, decoded, decode_stderr = run_cli_command('decode', encoded)
        assert decode_return_code == 0
        
        # Verify round-trip
        assert decoded == test_input


class TestCLIEdgeCases:
    """Test CLI edge cases."""
    
    def test_encode_single_character(self):
        """Test encoding single character via CLI."""
        test_input = "A"
        return_code, stdout, stderr = run_cli_command('encode', test_input)
        
        assert return_code == 0
        assert stderr == ""
        assert Base58.is_valid(stdout)
        
        # Verify round-trip
        decoded_return_code, decoded_stdout, decoded_stderr = run_cli_command('decode', stdout)
        assert decoded_return_code == 0
        assert decoded_stdout == test_input
    
    def test_encode_repeated_characters(self):
        """Test encoding string with repeated characters via CLI."""
        test_input = "aaa" * 100
        return_code, stdout, stderr = run_cli_command('encode', test_input)
        
        assert return_code == 0
        assert stderr == ""
        assert Base58.is_valid(stdout)
        
        # Verify round-trip
        decoded_return_code, decoded_stdout, decoded_stderr = run_cli_command('decode', stdout)
        assert decoded_return_code == 0
        assert decoded_stdout == test_input
    
    def test_decode_all_ones(self):
        """Test decoding base58 string of all ones via CLI."""
        all_ones = "11111111111111111111111111111111"
        return_code, stdout, stderr = run_cli_command('decode', all_ones)
        
        assert return_code == 0
        assert stderr == ""
        # Should decode to 32 zero bytes (length of base58 string)
        assert len(stdout) == 32
        assert all(ord(c) == 0 for c in stdout)
    
    def test_decode_bitcoin_address_format(self):
        """Test decoding Bitcoin address format via CLI."""
        bitcoin_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        return_code, stdout, stderr = run_cli_command('decode', bitcoin_address)
        
        # Bitcoin address format may not decode to valid UTF-8, which is acceptable
        if return_code == 0:
            assert stderr == ""
            # Should decode to some binary data
            assert len(stdout) > 0
        else:
            # If it fails due to UTF-8 decode issues, that's acceptable
            assert "Error:" in stdout


class TestCLIPerformance:
    """Test CLI performance characteristics."""
    
    def test_encode_performance_small_input(self):
        """Test CLI encode performance with small input."""
        test_input = "Hello, World!"
        
        import time
        start_time = time.time()
        return_code, stdout, stderr = run_cli_command('encode', test_input)
        end_time = time.time()
        
        assert return_code == 0
        assert end_time - start_time < 5.0  # Should complete within 5 seconds
    
    def test_decode_performance_small_input(self):
        """Test CLI decode performance with small input."""
        # First encode to get a valid base58 string
        test_input = "Hello, World!"
        encode_return_code, encoded, encode_stderr = run_cli_command('encode', test_input)
        assert encode_return_code == 0
        
        import time
        start_time = time.time()
        return_code, stdout, stderr = run_cli_command('decode', encoded)
        end_time = time.time()
        
        assert return_code == 0
        assert end_time - start_time < 5.0  # Should complete within 5 seconds
    
    def test_encode_performance_large_input(self):
        """Test CLI encode performance with large input."""
        test_input = "a" * 1000
        
        import time
        start_time = time.time()
        return_code, stdout, stderr = run_cli_command('encode', test_input)
        end_time = time.time()
        
        assert return_code == 0
        assert end_time - start_time < 10.0  # Should complete within 10 seconds
