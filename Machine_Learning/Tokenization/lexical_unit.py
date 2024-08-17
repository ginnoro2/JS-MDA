#!/usr/bin/python
"""
        Configuration file storing the dictionary TOKENS.
        Key: Esprima lexical unit (token);
        Value: Unique integer.
"""


TOKENS= {
    'Boolean': 0,
    '<end>': 1,
    'Identifier': 2,
    'Keyword': 3,
    'Null': 4,
    'Numeric': 5,
    'Punctuator': 6,
    'String': 7,
    'RegularExpression': 8,
    'Template': 9,
    'LineComment': 10,
    'BlockComment': 11,
    'document.write()': 12,
    'eval()': 13,
    'unescape()': 14,
    'SetCookie()': 15,
    'GetCookie()': 16,
    'newActiveXObject()': 17
}