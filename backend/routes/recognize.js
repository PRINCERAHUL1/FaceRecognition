const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');

router.post('/', (req, res) => {
    const pythonProcess = spawn('python', ['recognitioSystem/test.py']);

    let result = '';
    pythonProcess.stdout.on('data', (data) => {
        result += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        if (code === 0) {
            res.json({ result: result.trim() });
        } else {
            res.status(500).json({ result: 'Recognition failed' });
        }
    });
});

module.exports = router;
