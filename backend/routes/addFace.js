const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');

router.post('/add-face', (req, res) => {
    const name = req.body.name;
    if (!name || name.trim() === '') {
        return res.status(400).json({ message: 'Name is required' });
    }

    const pythonProcess = spawn('python', ['recognitioSystem/add_faces.py', name]);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        if (code === 0) {
            res.json({ message: `Face capturing for "${name}" started. Follow terminal instructions.` });
        } else {
            res.status(500).json({ message: 'Failed to add face.' });
        }
    });
});

module.exports = router;
