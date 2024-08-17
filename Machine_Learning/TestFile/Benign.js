// Example of a benign JavaScript script

// Function to calculate the factorial of a number
function factorial(n) {
    if (n === 0 || n === 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

// Function to display a message
function displayMessage(message) {
    console.log(message);
}

// Main script execution
function main() {
    const number = 5;
    const result = factorial(number);
    displayMessage(`The factorial of ${number} is ${result}.`);
}

// Call the main function to run the script
main();
