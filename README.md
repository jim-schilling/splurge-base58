# splurge-base58

A Python library for Base-58 encoding and decoding operations with both CLI and API interfaces.

## Features

- **Pure Python Implementation**: No external dependencies required
- **Bitcoin-Compatible Alphabet**: Uses the standard Bitcoin Base-58 alphabet
- **CLI Interface**: Command-line tool for quick encoding/decoding operations
- **API Interface**: Python class for programmatic use
- **Input Validation**: Comprehensive validation with meaningful error messages
- **Length Constraints**: Configurable input length limits for security
- **Unicode Support**: Full support for UTF-8 encoded strings
- **Error Handling**: Robust error handling with custom exception types
- **Performance Optimized**: Efficient algorithms for encoding and decoding

## Installation

```bash
pip install splurge-base58
```

## CLI Usage

The CLI provides a simple command-line interface for Base-58 operations.

### Basic Commands

```bash
# Encode a string to Base-58
python -m splurge_base58 encode "Hello, World!"

# Decode a Base-58 string
python -m splurge_base58 decode "JxF12TrwUP45BMd"
```

### Command Syntax

```bash
python -m splurge_base58 <command> <input>
```

**Commands:**
- `encode` - Convert input string to Base-58 encoding
- `decode` - Convert Base-58 string back to original data

**Constraints:**
- `encode`: Maximum input length is 2048 characters
- `decode`: Maximum input length is calculated based on maximum encode length

### Examples

```bash
# Encode various types of data
python -m splurge_base58 encode "Hello, World!"
python -m splurge_base58 encode "1234567890"
python -m splurge_base58 encode "Special chars: !@#$%^&*()"

# Decode Base-58 strings
python -m splurge_base58 decode "JxF12TrwUP45BMd"
python -m splurge_base58 decode "2NEpo7TZRRrLZSi2U"
python -m splurge_base58 decode "11111111111111111111111111111111"

# Error handling examples
python -m splurge_base58 decode "invalid!@#"  # Invalid Base-58
python -m splurge_base58 encode ""            # Empty input
```

### Error Handling

The CLI provides clear error messages for various scenarios:

- **Invalid Base-58 string**: When decode input contains invalid characters
- **Empty input**: When encode input is empty
- **Input too long**: When input exceeds maximum length constraints
- **Unknown command**: When an invalid command is provided

## API Usage

The `Base58` class provides a comprehensive API for Base-58 operations.

### Basic Usage

```python
from splurge_base58.base58 import Base58, Base58Error

# Encode data
data = "Hello, World!".encode('utf-8')
encoded = Base58.encode(data)
print(encoded)  # Output: JxF12TrwUP45BMd

# Decode data
decoded = Base58.decode(encoded)
original = decoded.decode('utf-8')
print(original)  # Output: Hello, World!
```

### Class Methods

#### `Base58.encode(data: bytes) -> str`

Encodes binary data to a Base-58 string.

```python
# Encode string data
text = "Hello, World!"
data = text.encode('utf-8')
encoded = Base58.encode(data)

# Encode binary data
binary_data = b'\x00\x01\x02\x03'
encoded = Base58.encode(binary_data)

# Encode hash data
import hashlib
hash_data = hashlib.sha256(b"test").digest()
encoded = Base58.encode(hash_data)
```

#### `Base58.decode(base58_data: str) -> bytes`

Decodes a Base-58 string back to binary data.

```python
# Decode to string
encoded = "JxF12TrwUP45BMd"
decoded = Base58.decode(encoded)
text = decoded.decode('utf-8')

# Decode binary data
encoded = "11111111111111111111111111111111"
decoded = Base58.decode(encoded)
print(decoded.hex())  # Output: 00000000000000000000000000000000
```

#### `Base58.is_valid(base58_data: str) -> bool`

Validates if a string is valid Base-58.

```python
# Valid Base-58 strings
Base58.is_valid("JxF12TrwUP45BMd")  # True
Base58.is_valid("11111111111111111111111111111111")  # True

# Invalid Base-58 strings
Base58.is_valid("invalid!@#")  # False
Base58.is_valid("")  # False
```

### Error Handling

The API uses custom exception types for different error scenarios:

```python
from splurge_base58.base58 import Base58, Base58Error, Base58TypeError, Base58ValidationError

try:
    # Encode with invalid input type
    Base58.encode("not bytes")  # Raises Base58TypeError
    
    # Encode empty data
    Base58.encode(b"")  # Raises Base58ValidationError
    
    # Decode invalid Base-58
    Base58.decode("invalid!@#")  # Raises Base58ValidationError
    
except Base58TypeError as e:
    print(f"Type error: {e}")
except Base58ValidationError as e:
    print(f"Validation error: {e}")
except Base58Error as e:
    print(f"Base-58 error: {e}")
```

### Practical Examples

#### Encoding JSON Data

```python
import json
from splurge_base58.base58 import Base58

# Encode JSON payload
data = {
    "user_id": 12345,
    "timestamp": "2024-01-15T10:30:00Z",
    "action": "login"
}

json_string = json.dumps(data)
json_bytes = json_string.encode('utf-8')
encoded = Base58.encode(json_bytes)

# Decode and verify
decoded = Base58.decode(encoded)
decoded_json = decoded.decode('utf-8')
restored_data = json.loads(decoded_json)
```

#### Encoding File Data

```python
from splurge_base58.base58 import Base58

# Encode file header (example: PNG header)
file_header = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
encoded = Base58.encode(file_header)

# Decode file data
decoded = Base58.decode(encoded)
print(decoded.hex())  # Output: 89504e470d0a1a0a0000000d494844520000000100000001
```

#### Encoding Hash Values

```python
import hashlib
from splurge_base58.base58 import Base58

# Encode SHA-256 hash
password = "password123"
hash_data = hashlib.sha256(password.encode('utf-8')).digest()
encoded = Base58.encode(hash_data)

# Decode hash
decoded = Base58.decode(encoded)
print(decoded.hex())  # Output: 240be01fab5649d2beb87e2d6a5574d
```

### Performance Considerations

The implementation is optimized for performance:

- **Efficient algorithms**: Uses optimized conversion methods
- **Memory efficient**: Minimal memory overhead during operations
- **Fast validation**: Quick validation of Base-58 strings

For large datasets, consider processing data in chunks if needed.

## Examples

See the `examples/` directory for complete working examples:

- `cli_usage.py` - CLI end-to-end workflow examples
- `api_usage.py` - API end-to-end workflow examples

Run the examples:

```bash
# CLI examples
python examples/cli_usage.py

# API examples
python examples/api_usage.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
