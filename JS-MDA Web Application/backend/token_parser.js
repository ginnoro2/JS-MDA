const fs = require('fs');
const esprima = require('esprima');

const inputFile = process.argv[2];
const outputFile = process.argv[3];

if (!inputFile || !outputFile) {
    console.error('Input or output file not specified');
    process.exit(1);
}

// Read input JavaScript file
fs.readFile(inputFile, 'utf8', (err, javascriptCode) => {
    if (err) {
        console.error('Error reading input file:', err);
        process.exit(1);
    }

    // Tokenization
    const tokens = [];
    try {
        const lexer = esprima.tokenize(javascriptCode);
        lexer.forEach(token => {
            tokens.push({
                type: token.type,
                value: token.value
            });
        });
    } catch (error) {
        console.error('Error during tokenization:', error);
        process.exit(1);
    }

    // Parsing for syntactic features
    const syntacticFeatures = [];
    try {
        const parsed = esprima.parseScript(javascriptCode, { tokens: true });
        traverse(parsed, node => {
            if (node.type) {
                syntacticFeatures.push({
                    type: node.type
                });
            }
        });
    } catch (error) {
        console.error('Error during parsing:', error);
        process.exit(1);
    }

    // Write results to JSON file
    fs.writeFile(outputFile, JSON.stringify({
        tokens: tokens,
        syntactic_features: syntacticFeatures
    }, null, 2), (err) => {
        if (err) {
            console.error('Error writing JSON file:', err);
            process.exit(1);
        }
        console.log('Output written to', outputFile);
    });
});

// Helper function to traverse nodes
function traverse(node, callback) {
    if (Array.isArray(node)) {
        node.forEach(child => traverse(child, callback));
    } else if (node && typeof node === 'object') {
        callback(node);
        Object.values(node).forEach(value => traverse(value, callback));
    }
}
