/*const fs = require('fs');
const esprima = require('esprima');

const jsFilePath = process.argv[2];
const outputFilePath = process.argv[3];

const code = fs.readFileSync(jsFilePath, 'utf8');
const tokens = esprima.tokenize(code);

let output = tokens.map(token => `${token.type},${token.value}`).join('\n');

fs.writeFileSync(outputFilePath, output, 'utf8');
*/
const fs = require('fs');
const esprima = require('esprima');

const filePath = process.argv[2];
const outputPath = process.argv[3];

try {
    const code = fs.readFileSync(filePath, 'utf8');
    const tokens = esprima.tokenize(code, { tolerant: true });
    
    const tokenStrings = tokens.map(token => `${token.type},${token.value}`).join('\n');
    fs.writeFileSync(outputPath, tokenStrings, 'utf8');
    
    console.log('Tokenization complete.');
} catch (error) {
    console.error(`Error processing file ${filePath}: ${error.message}`);
    console.error(error);
    process.exit(1);  // Exit with a non-zero code to indicate failure
}
