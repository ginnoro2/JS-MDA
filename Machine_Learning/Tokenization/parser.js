// syntactic_analyzer.js
const fs = require('fs');
const esprima = require('esprima');

const jsFilePath = process.argv[2];
const outputFilePath = process.argv[3];

const code = fs.readFileSync(jsFilePath, 'utf8');
const syntaxTree = esprima.parseScript(code, { range: true });

function traverse(node, output) {
    if (node.type) {
        output.push(node.type);
    }
    for (let key in node) {
        if (node[key] && typeof node[key] === 'object') {
            traverse(node[key], output);
        }
    }
}

let output = [];
traverse(syntaxTree, output);

fs.writeFileSync(outputFilePath, output.join('\n'), 'utf8');
