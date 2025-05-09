const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const recognizeRoute = require('./routes/recognize');
const addFaceRoute = require('./routes/addFace');
require('dotenv').config();  // Load environment variables

const app = express();
app.use(cors());
app.use(express.json());
app.use(bodyParser.json());


app.use('/recognize', recognizeRoute);
app.use('/', addFaceRoute);

app.get('/', (req, res) => {
    res.send('Face recognition');
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
