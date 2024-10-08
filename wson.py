import re

class WSONParseError(Exception):
    pass

def parse_wson(wson_str):
    wson_str = remove_comments(wson_str)
    return convert_wson_to_dict(wson_str)

def remove_comments(wson_str):
    lines = wson_str.splitlines()
    cleaned_lines = []
    for line in lines:
        comment_index = line.find('//')
        hash_index = line.find('#')
        if comment_index != -1:
            line = line[:comment_index]
        elif hash_index != -1:
            line = line[:hash_index]
        cleaned_lines.append(line.rstrip())
    return '\n'.join(cleaned_lines)

def parse_value(value):
    value = value.strip()
    if not value:
        return None
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]  # 문자열
    elif value.lower() in ['true', 'false']:
        return value.lower() == 'true'  # 불리언
    elif re.match(r'^-?\d+(\.\d+)?$', value):
        return float(value) if '.' in value else int(value)
    elif value.startswith('{') and value.endswith('}'):
        return convert_wson_to_dict(value)  # 중첩 WSON 호출
    elif value.startswith('[') and value.endswith(']'):
        return parse_array(value)  # 배열 파싱 함수 호출
    raise WSONParseError(f"Invalid value: {value}")

def parse_array(array_str):
    array_str = array_str[1:-1].strip()  # [] 제거
    items = []
    current_item = ''
    brace_count = 0
    bracket_count = 0
    
    for char in array_str:
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
        elif char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1
        
        if char == ',' and brace_count == 0 and bracket_count == 0:
            items.append(parse_value(current_item.strip()))
            current_item = ''
        else:
            current_item += char
    
    if current_item.strip():
        items.append(parse_value(current_item.strip()))
    
    return items

def convert_wson_to_dict(wson_str):
    wson_str = wson_str.strip()
    if not (wson_str.startswith('{') and wson_str.endswith('}')):
        raise WSONParseError("WSON format must start and end with curly braces.")
    
    wson_str = wson_str[1:-1]  # {} 제거
    data = {}
    key = ''
    value = ''
    in_key = True
    brace_count = 0
    bracket_count = 0
    
    for char in wson_str:
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
                data[key.strip()] = parse_value(value.strip())
                key = ''
                value = ''
                in_key = True
        elif in_key:
            key += char
        else:
            value += char
    
    if key:
        data[key.strip()] = parse_value(value.strip())
    
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

if __name__ == "__main__":
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
    
    parsed_data = parse_wson(wson_data)
    print("Parsed Data:", parsed_data)

    wson_output = serialize_wson(parsed_data)
    print("\nSerialized WSON:\n", wson_output)