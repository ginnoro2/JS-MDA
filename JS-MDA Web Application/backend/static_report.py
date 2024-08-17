import csv
import argparse
import hashlib
import os

def calculate_md5(file_path):
    with open(file_path, 'rb') as file:
        file_hash = hashlib.md5()
        while chunk := file.read(8192):
            file_hash.update(chunk)
        return file_hash.hexdigest()

def analyze_js_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        num_lines = content.count('\n') + 1
        num_functions = content.count('function')
        num_variables = content.count('var') + content.count('let') + content.count('const')
        num_strings = content.count('"') + content.count("'") // 2
        keywords = {
            'eval': content.count('eval'),
            'document.write': content.count('document.write'),
            'setTimeout': content.count('setTimeout'),
            'setInterval': content.count('setInterval'),
            'escape': content.count('escape'),
        }
        suspicious_patterns = {
            'Obfuscation Detected': 'Yes' if 'eval' in content or 'escape' in content else 'No',
            'Dynamic Code Execution': 'Yes' if 'document.write' in content else 'No',
            'Network Requests': 'Yes' if 'iframe' in content else 'No',
            'Cookie Access': 'Yes' if 'document.cookie' in content else 'No'
        }
        return {
            'num_lines': num_lines,
            'num_functions': num_functions,
            'num_variables': num_variables,
            'num_strings': num_strings,
            'keywords': keywords,
            'suspicious_patterns': suspicious_patterns
        }

def generate_report(file_path):
    file_size = os.path.getsize(file_path) / 1024  # File size in KB
    md5_hash = calculate_md5(file_path)
    analysis = analyze_js_file(file_path)
    
    report = f"""File Name: {os.path.basename(file_path)}
Basic Information:
    • File Size: {file_size:.2f} KB
    • MD5 Hash: {md5_hash}
Lexical Features:
    • Number of Lines: {analysis['num_lines']}
    • Number of Functions: {analysis['num_functions']}
    • Number of Variables: {analysis['num_variables']}
    • Number of Strings: {analysis['num_strings']}
Syntactic Features:
    • Keywords Frequency:"""
    
    for keyword, count in analysis['keywords'].items():
        report += f"\n    ◦ {keyword}: {count}"
    
    report += "\n    • Suspicious Patterns:"
    
    for pattern, detected in analysis['suspicious_patterns'].items():
        report += f"\n    ◦ {pattern}: {detected}"
    
    return report

def main():
    parser = argparse.ArgumentParser(description='Generate Static Report for JavaScript File')
    parser.add_argument('js_file', help='Path to the JavaScript file')
    args = parser.parse_args()
    
    report = generate_report(args.js_file)
    print(report)

if __name__ == "__main__":
    main()
