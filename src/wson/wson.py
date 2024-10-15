from datetime import datetime
import re

class WSONParseError(Exception):
    def __init__(self, message, line=None, column=None):
        self.line = line
        self.column = column
        super().__init__(f"{message} (line {line}, column {column})" if line and column else message)

class WSONSerializeError(Exception):
    pass

def parse_wson(wson_str):
    cleaned_wson = remove_comments(wson_str)
    return convert_wson_to_dict(cleaned_wson)

def remove_comments(wson_str):
    lines = wson_str.splitlines()
    cleaned_lines = []
    in_block_comment = False

    for line in lines:
        if in_block_comment:
            end_index = line.find('*/')
            if end_index != -1:
                line = line[end_index + 2:]
                in_block_comment = False
            else:
                continue
        while '/*' in line:
            start_index = line.find('/*')
            end_index = line.find('*/', start_index + 2)
            if end_index != -1:
                line = line[:start_index]
            else:
                line = line[:start_index]
                in_block_comment = True
                break
        comment_index = line.find('//')
        hash_index = line.find('#')
        if comment_index != -1:
            line = line[:comment_index]
        elif hash_index != -1:
            line = line[:hash_index]
        if line.strip():
            cleaned_lines.append(line.rstrip())
    return '\n'.join(cleaned_lines)

def parse_value(value, line, column):
    value = value.strip()
    if not value:
        return None
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]  # 문자열
    elif value.lower() in ['true', 'false']:
        return value.lower() == 'true'  # 불리언
    elif re.match(r'^-?\d+(\.\d+)?$', value):
        return float(value) if '.' in value else int(value)
    elif re.match(r'^\d{4}-\d{2}-\d{2}$', value):  # 날짜 (YYYY-MM-DD)
        return datetime.strptime(value, '%Y-%m-%d').date()
    elif re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', value):  # 날짜+시간 (YYYY-MM-DD HH:MM:SS)
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    elif re.match(r'^\d+(\.\d+)+$', value):  # 버전 (예: 1.0.0)
        return tuple(map(int, value.split('.')))
    elif value.startswith('{') and value.endswith('}'):
        return convert_wson_to_dict(value, line, column)  # 중첩 WSON 호출
    elif value.startswith('[') and value.endswith(']'):
        return parse_array(value, line, column)  # 배열 파싱 함수 호출
    raise WSONParseError(f"Invalid value: {value}", line, column)

def parse_array(array_str, line, column):
    array_str = array_str[1:-1].strip()  # [] 제거
    items = []
    current_item = ''
    brace_count = 0
    bracket_count = 0

    for i, char in enumerate(array_str):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
        elif char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1

        if char == ',' and brace_count == 0 and bracket_count == 0:
            items.append(parse_value(current_item.strip(), line, column + i))
            current_item = ''
        else:
            current_item += char

    if current_item.strip():
        items.append(parse_value(current_item.strip(), line, column + len(array_str)))

    return items

def convert_wson_to_dict(wson_str, start_line=1, start_column=1):
    wson_str = wson_str.strip()
    if not (wson_str.startswith('{') and wson_str.endswith('}')):
        raise WSONParseError("WSON format must start and end with curly braces.", start_line, start_column)

    wson_str = wson_str[1:-1]  # {} 제거
    data = {}
    key = ''
    value = ''
    in_key = True
    brace_count = 0
    bracket_count = 0
    line = start_line
    column = start_column

    for i, char in enumerate(wson_str):
        if char == '\n':
            line += 1
            column = start_column
            continue

        if char in ['=', ':'] and in_key and brace_count == 0 and bracket_count == 0:
            in_key = False
            continue

        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
        elif char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1

        if char == ',' and brace_count == 0 and bracket_count == 0:
            if key:
                data[key.strip()] = parse_value(value.strip(), line, column + i)
                key = ''
                value = ''
                in_key = True
        elif in_key:
            key += char
        else:
            value += char

    if key:
        data[key.strip()] = parse_value(value.strip(), line, column + len(wson_str))

    return data

def serialize_wson(data, indent=''):
    return '{\n' + serialize_dict(data, indent + '    ') + '\n' + indent + '}'

def serialize_dict(data, indent=''):
    items = []
    for key, value in data.items():
        if isinstance(value, dict):
            items.append(f'{indent}{key} = ' + serialize_wson(value, indent))
        elif isinstance(value, list):
            items.append(f'{indent}{key} = [\n' + serialize_list(value, indent + '    ') + f'\n{indent}]')
        elif isinstance(value, str):
            items.append(f'{indent}{key} = "{value}"')
        elif value is None:
            items.append(f'{indent}{key} = null')
        else:
            items.append(f'{indent}{key} = {value}')
    return ',\n\n'.join(items)

def serialize_list(data, indent=''):
    items = []
    for item in data:
        if isinstance(item, dict):
            items.append(indent + serialize_wson(item, indent))
        elif isinstance(item, list):
            items.append(indent + '[\n' + serialize_list(item, indent + '    ') + f'\n{indent}]')
        elif isinstance(item, str):
            items.append(f'{indent}"{item}"')
        elif item is None:
            items.append(f'{indent}null')
        else:
            items.append(f'{indent}{item}')
    return ',\n'.join(items)

def dumps(data):
    """
    Serialize Python object to WSON string.

    :param data: Python object (dict or list) to serialize.
    :return: WSON formatted string.
    """
    return serialize_wson(data)

def loads(wson_str):
    """
    Parse WSON string to Python object.

    :param wson_str: WSON formatted string.
    :return: Python object (dict or list).
    :raises WSONParseError: If the WSON format is invalid.
    """
    return parse_wson(wson_str)

def validate_wson(wson_str):
    """
    Validate a WSON string for correctness.

    :param wson_str: WSON formatted string.
    :return: True if valid, raises WSONParseError if invalid.
    """
    try:
        parse_wson(wson_str)
        return True
    except WSONParseError:
        return False

def tests():
    wson_data = """
    {
        /*
            Hello Block Comment
        */
        status = "success",
        code = 200,
        message = "Data retrieved successfully",
        version = 1.0.0,
        release_date = 2024-10-09,
        user = {
            id = 123,
            name = "John Doe",
            email = "john@example.com",
            age = 25,
            joined = 2023-01-15 09:00:00
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

    print("Testing `loads` function...")
    try:
        parsed_data = loads(wson_data)
        print("Parsed Data:", parsed_data)
    except WSONParseError as e:
        print("Parsing Error:", e)

    print("\nTesting `dumps` function...")
    try:
        wson_output = dumps(parsed_data)
        print("\nSerialized WSON:\n", wson_output)
    except WSONSerializeError as e:
        print("Serialization Error:", e)

    print("\nTesting `validate_wson` function...")
    valid = validate_wson(wson_data)
    print("Is valid WSON:", valid)

if __name__ == "__main__":
    tests()