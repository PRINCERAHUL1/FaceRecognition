// const { exec } = require('child_process');

// // Function to call Python script for face recognition
// const recognizeFace = (req, res) => {
//     const { imagePath } = req.body;

//     // Call Python script with image path
//     exec(`python3 backend/recognition-system/face_recognition.py ${imagePath}`, (error, stdout, stderr) => {
//         if (error) {
//             console.error(`exec error: ${error}`);
//             return res.status(500).json({ message: 'Error in face recognition' });
//         }
//         if (stderr) {
//             console.error(`stderr: ${stderr}`);
//             return res.status(500).json({ message: 'Error in face recognition' });
//         }
//         // Return the result from the Python script
//         res.status(200).json({ result: stdout.trim() });
//     });
// };

// module.exports = { recognizeFace };

// controllers/recognitionController.js


// const { spawn } = require('child_process');
// const path = require('path');

// const recognizeFace = async (req, res) => {
//     try {
//         const imageFile = req.file;

//         if (!imageFile) {
//             return res.status(400).json({ message: 'No image file uploaded' });
//         }

//         const imagePath = path.join(__dirname, '..', 'uploads', imageFile.filename);

//         // Correct and absolute path to faceRecognition.py
//         const scriptPath = path.join(__dirname, '..', 'recognitioSystem', 'faceRecognition.py');

//         const pythonProcess = spawn('python', [scriptPath, imagePath]);

//         let output = '';
//         pythonProcess.stdout.on('data', (data) => {
//             output += data.toString();
//         });

//         pythonProcess.stderr.on('data', (data) => {
//             console.error(`Python error: ${data}`);
//         });

//         pythonProcess.on('close', (code) => {
//             if (code === 0) {
//                 res.status(200).json({ result: output.trim() });
//             } else {
//                 res.status(500).json({ message: 'Recognition failed' });
//             }
//         });

//     } catch (error) {
//         console.error(error);
//         res.status(500).json({ message: 'Internal server error' });
//     }
// };

// module.exports = { recognizeFace };


const { spawn } = require('child_process');
const path = require('path');

const recognizeFace = (req, res) => {
  const imagePath = req.file.path;

  const process = spawn('python', [
    path.join(__dirname, '../recognitionSystem/faceRecognition.py'),
    imagePath
  ]);

  let result = '';

  process.stdout.on('data', (data) => {
    result += data.toString();
  });

  process.on('close', () => {
    res.status(200).json({ name: result.trim() }); // Return recognized name
  });

  process.stderr.on('data', (err) => {
    console.error(err.toString());
    res.status(500).json({ error: 'Python error' });
  });
};
