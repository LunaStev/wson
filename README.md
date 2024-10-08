# WSON (Web Simple Object Notation)

WSON is a simple, readable data interchange format that combines the best features of JSON and YAML while addressing some of their limitations.

## Features

- Simple and intuitive syntax
- Supports comments (both // and # styles)
- Preserves the original formatting when possible
- Easy to read and write for humans
- Supports nested objects and arrays
- Handles strings, numbers, booleans, and null values

## Installation

You can install WSON using pip:

```
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