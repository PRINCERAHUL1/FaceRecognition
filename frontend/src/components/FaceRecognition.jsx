import React, { useState } from 'react';
import axios from 'axios';

const FaceRecognition = () => {
    const [result, setResult] = useState('');

    const handleRecognition = async () => {
        try {
            const response = await axios.post('https://facerecognition-vzuf.onrender.com/recognize');
            setResult(response.data.result);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <button onClick={handleRecognition}>Recognize Face</button>
            {result && <p style={{ marginTop: '20px' }}>Result: {result}</p>}
        </div>
    );
};

export default FaceRecognition;


// import React, { useRef, useState } from 'react';
// import axios from 'axios';

// const FaceRecognition = () => {
//     const videoRef = useRef(null);
//     const canvasRef = useRef(null);
//     const [result, setResult] = useState('');

//     const startCamera = async () => {
//         try {
//             const stream = await navigator.mediaDevices.getUserMedia({ video: true });
//             if (videoRef.current) {
//                 videoRef.current.srcObject = stream;
//             }
//         } catch (error) {
//             console.error('Error accessing camera:', error);
//         }
//     };

//     const handleRecognition = async () => {
//         await startCamera();
//     };

//     const handleAddFace = async () => {
//         const name = prompt('Enter the name of the person:');
//         if (!name || name.trim() === '') {
//             alert('Name is required!');
//             return;
//         }

//         try {
//             const response = await axios.post('http://localhost:5000/add-face', { name });
//             alert(response.data.message);
//         } catch (error) {
//             console.error('Add face error:', error);
//             alert('Failed to add face.');
//         }
//     };

//     return (
//         <div style={{ textAlign: 'center', padding: '20px' }}>
//             <video ref={videoRef} autoPlay style={{ width: '400px' }} />
//             <canvas ref={canvasRef} style={{ display: 'none' }} />

//             <div style={{ marginTop: '20px' }}>
//                 <button onClick={handleRecognition}>Recognize</button>
//                 <button onClick={handleAddFace} style={{ marginLeft: '10px' }}>Add Face</button>
//             </div>

//             {result && (
//                 <div style={{ marginTop: '20px' }}>
//                     <p><strong>Result:</strong> {result}</p>
//                 </div>
//             )}
//         </div>
//     );
// };

// export default FaceRecognition;
