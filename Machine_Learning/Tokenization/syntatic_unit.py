
#!/usr/bin/python

"""
        Configuration file storing the dictionary features.
        Key: Esprima syntactic unit;
        Value: Unique integer provided.
"""


features = {
    'ArrayExpression': 0,
    'ArrayPattern': 1,
    'ArrowFunctionExpression': 2,
    'AssignmentExpression': 3,
    'AssignmentPattern': 4,
    'AwaitExpression': 5,
    'BinaryExpression': 6,
    'BlockStatement': 7,
    'BreakStatement': 8,
    'CallExpression': 9,
    'CatchClause': 10,
    'ClassBody': 11,
    'ClassDeclaration': 12,
    'ClassExpression': 13,
    'ConditionalExpression': 14,
    'ContinueStatement': 15,
    'DebuggerStatement': 16,
    'DoWhileStatement': 17,
    'EmptyStatement': 18,
    'ExportAllDeclaration': 19,
    'ExportDefaultDeclaration': 20,
    'ExportNamedDeclaration': 21,
    'ExportSpecifier': 22,
    'ExpressionStatement': 23,
    'ForInStatement': 24,
    'ForOfStatement': 25,
    'ForStatement': 26,
    'FunctionDeclaration': 27,
    'FunctionExpression': 28,
    'Identifier': 29,
    'IfStatement': 30,
    'Import': 31,
    'ImportDeclaration': 32,
    'ImportDefaultSpecifier': 33,
    'ImportNamespaceSpecifier': 34,
    'ImportSpecifier': 35,
    'LabeledStatement': 36,
    'Literal': 37,
    'LogicalExpression': 38,
    'MemberExpression': 39,
    'MetaProperty': 40,
    'MethodDefinition': 41,
    'NewExpression': 42,
    'ObjectExpression': 43,
    'ObjectPattern': 44,
    'Program': 45,
    'Property': 46,
    'RestElement': 47,
    'ReturnStatement': 48,
    'SequenceExpression': 49,
    'SpreadElement': 50,
    'Super': 51,
    'SwitchCase': 52,
    'SwitchStatement': 53,
    'TaggedTemplateExpression': 54,
    'TemplateElement': 55,
    'TemplateLiteral': 56,
    'ThisExpression': 57,
    'ThrowStatement': 58,
    'TryStatement': 59,
    'UnaryExpression': 60,
    'UpdateExpression': 61,
    'VariableDeclaration': 62,
    'VariableDeclarator': 63,
    'WhileStatement': 64,
    'WithStatement': 65,
    'YieldExpression': 66,
    'Line': 67,
    'Block': 68,
    'String': 69,
    'Int': 70,
    'Numeric': 71,
    'Bool': 72,
    'Null': 73,
    'RegExp': 74,
    'document.write()': 75,
    'eval()': 76,
    'unescape()': 77,
    'SetCookie()': 78,
    'GetCookie()': 79,
    'newActiveXObject()': 80
}