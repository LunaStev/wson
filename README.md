# WSON (Web Simple Object Notation)

[![GitHub](https://img.shields.io/github/license/LunaStev/wson)](https://mit-license.org/)
[![YouTube](https://img.shields.io/badge/YouTube-LunaStev-red.svg?logo=youtube)](https://www.youtube.com/@luna-bee)

WSON is a simple, readable data interchange format that combines the best features of JSON and YAML while addressing some of their limitations.

## Features

| Feature                        | Status      | Description                                |
|-------------------------------|-------------|--------------------------------------------|
| Syntax                        | Implemented | The basic syntax of WSON is implemented.  |
| Comment Support (// and # styles) | Implemented | The ability to remove comments is implemented. |
| Original Formatting Preservation | Not Implemented | The functionality to preserve original formatting is not explicitly implemented. |
| Nested Objects and Arrays Support | Implemented | Capable of parsing and serializing nested objects and arrays. |
| String, Number, Boolean, and Null Handling | Implemented | Can handle various data types.             |

## Language Support

| Language                       | Status         | Badges                      |
|-------------------------------|----------------|-----------------------------|
| Python                        | **Implemented**     | ![PyPI](https://img.shields.io/pypi/v/wson.svg) ![PyPI](https://img.shields.io/pypi/pyversions/wson.svg) |
| JavaScript                    | Not Implemented  |                             |
| Java                          | Not Implemented  |                             |
| C#                            | Not Implemented  |                             |
| Ruby                          | Not Implemented  |                             |
| Go                            | Not Implemented  |                             |
| C                             | Not Implemented  |                             |
| C++                           | Not Implemented  |                             |
| PHP                           | Not Implemented  |                             |

## Installation

You can install WSON using pip:

```bash
pip install wson
```

## Usage

Here's a quick example of how to use WSON in your Python projects:

```python
import wson

# Parse WSON string
wson_data = """
{
    status = "success",
    code = 200,
    message = "Data retrieved successfully",

    user = {
        id = 123,
        name = "John Doe",
        email = "john@example.com",
        age = 25
    },

    tasks = [
        {
            task_id = 1,
            title = "Complete project report",
            status = "in-progress",
            due_date = "2024-10-15"
        },
        {
            task_id = 2,
            title = "Review team feedback",
            status = "pending",
            due_date = "2024-10-20"
        }
    ]
}
"""

# Parse WSON to Python dictionary
parsed_data = wson.parse_wson(wson_data)
print(parsed_data)

# Serialize Python dictionary to WSON
wson_output = wson.serialize_wson(parsed_data)
print(wson_output)
```

## Why WSON?

WSON addresses some limitations of JSON and YAML:

1. Unlike JSON, WSON supports comments, making it more readable and self-documenting.
2. WSON has a simpler syntax compared to YAML, reducing the chance of indentation errors.
3. WSON preserves the original formatting when possible, unlike JSON which often alters the structure.
4. WSON is more concise than JSON, omitting unnecessary quotation marks for keys.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
