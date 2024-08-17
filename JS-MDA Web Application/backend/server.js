const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bodyParser = require('body-parser');
const { exec } = require('child_process');

const app = express();

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Connect to MongoDB
/*mongoose.connect('mongodb://localhost:27017/mern-stack-app', { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('MongoDB connected...'))
    .catch(err => console.log(err));*/

// API Route for text input (previous example)
app.post('/api/submit', async (req, res) => {
    const { text } = req.body;
    const newText = new Text({ content: text });
    await newText.save();
    res.json({ message: 'Text received!', data: newText });
});

// API Route for scraping
app.post('/api/scrape', (req, res) => {
    const url = req.body.url;
    if (!url) {
        return res.status(400).json({ error: 'URL is required' });
    }

    // Specify the full path to the Python executable
    const pythonPath = '/opt/homebrew/bin/python3.10'; // Update this to your Python path
    const command = `${pythonPath} scrape.py`;


    exec(command, (err, stdout, stderr) => {
        if (err) {
            console.error(`exec error: ${err}`);
            return res.status(500).json({ error: err.message });
        }
        try {
            const output = JSON.parse(stdout);
            res.json(output);
        } catch (parseErr) {
            res.status(500).json({ error: 'Failed to parse Python script output' });
        }
    });
});

// Start the server
const PORT = process.env.PORT || 1000;
app.listen(PORT, () => console.log(`Server started on port ${PORT}`));
