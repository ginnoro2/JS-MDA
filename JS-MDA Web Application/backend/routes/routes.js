const express = require('express');
const router = express.Router();

// Example route
router.get('/', (req, res) => {
  res.send('Get all routes');
});

module.exports = router;
