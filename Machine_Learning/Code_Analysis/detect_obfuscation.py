import re

def detect_obfuscation(js_code):
    # Patterns for common obfuscation methods
    hex_pattern = re.compile(r'\\x[0-9a-fA-F]{2}')
    unicode_pattern = re.compile(r'\\u[0-9a-fA-F]{4}')
    string_manipulation_pattern = re.compile(r'["\']\[\w+\]')
    base64_pattern = re.compile(r'([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?')
    eval_pattern = re.compile(r'\beval\s*\(')
    char_code_pattern = re.compile(r'String\.fromCharCode')

    # More sophisticated patterns
    long_strings_pattern = re.compile(r'["\'][^"\']{20,}["\']')  # Very long strings
    excessive_concatenation_pattern = re.compile(r'(?:\+[^+]){5,}')  # Excessive concatenation
    obfuscated_function_pattern = re.compile(r'function\s*\(\w+\)\s*\{')
    excessive_obfuscation_pattern = re.compile(r'(?:\\x[0-9a-fA-F]{2}|\\u[0-9a-fA-F]{4}|fromCharCode|\beval\s*\().{20,}')

    # Check for presence of patterns
    hex_match = re.search(hex_pattern, js_code)
    unicode_match = re.search(unicode_pattern, js_code)
    string_manipulation_match = re.search(string_manipulation_pattern, js_code)
    base64_match = re.search(base64_pattern, js_code)
    eval_match = re.search(eval_pattern, js_code)
    char_code_match = re.search(char_code_pattern, js_code)
    long_strings_match = re.search(long_strings_pattern, js_code)
    excessive_concatenation_match = re.search(excessive_concatenation_pattern, js_code)
    obfuscated_function_match = re.search(obfuscated_function_pattern, js_code)
    excessive_obfuscation_match = re.search(excessive_obfuscation_pattern, js_code)

    obfuscation_patterns = [
        hex_match, unicode_match, string_manipulation_match, base64_match, 
        eval_match, char_code_match, long_strings_match, 
        excessive_concatenation_match, obfuscated_function_match,
        excessive_obfuscation_match
    ]

    obfuscation_score = sum(1 for match in obfuscation_patterns if match)

    # Determine if code is obfuscated based on the number of detected patterns
    if obfuscation_score > 3:  # Adjust threshold as needed
        return True
    return False

def detect_base64_encoded_from_file(filename):
    try:
        with open(filename, 'r') as file:
            txt = file.read().strip()

        # Check if the content is Base64 encoded
        base64_pattern = re.compile(r'^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$')
        if re.search(base64_pattern, txt):
            return "Encoded"
        else:
            return "Non encoded"

    except FileNotFoundError:
        return f"Error: File '{filename}' not found."
    except Exception as e:
        return f"An error occurred: {e}"


def main():
    try:
        with open('tmp.txt', 'r') as file:
            js_code = file.read().strip()
        is_obfuscated = detect_obfuscation(js_code)

        if is_obfuscated:
            print("The JavaScript code appears to be obfuscated.")
        else:
            print("The JavaScript code does not appear to be obfuscated.")
            
        base64_status = detect_base64_encoded_from_file('tmp.txt')
        print(f"Base64 status:{base64_status}.")
    except FileNotFoundError:
        print(f"Error: File 'tmp.txt' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
