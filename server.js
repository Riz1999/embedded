const express = require('express')
const cors = require('cors')
const path = require('path')
const fs = require('fs')
const multer = require('multer');
const { exec } = require('child_process');


const app = express()

// middleware
// app.use(cors())

app.use(express.json())

app.use(cors('*'));
app.options('*', cors());

const uploadDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir, { recursive: true });
}

// Define a storage strategy for multer
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        // Define the directory where uploaded files will be stored
        cb(null, uploadDir);
    },
    filename: function (req, file, cb) {
        // Define the filename for the uploaded file
        //   cb(null, Date.now() + '-' + file.originalname);
        cb(null, Date.now() + '-' + '.png');
    },
});

// Create a multer instance with the storage configuration
const upload = multer({ storage: storage });



app.post('/apparel', upload.single('screenshot'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ message: 'No file uploaded.' });
        }

        // Access the uploaded file using req.file
        const uploadedFile = req.file.path;
        console.log(uploadedFile)

        const pythonFile = path.join(__dirname, 'video.py');
        const args = [`${uploadedFile}`];
        // const args = [uploadedFile, "Test"];

        const command = `python3 ${pythonFile} ${args.join(' ')}`;
        console.log(command)
        // const command = `python3 --version`;
        //   console.log("before exex")
        await exec(command, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error executing the Python script: ${error}`);
                return;
            }

            console.log('Python script output:');
            console.log(stdout);

            if (stderr) {
                console.error('Python script error:');
                console.error(stderr);
            }
            fs.unlink(uploadedFile, (err) => {
                if (err) {
                    console.error('Error deleting file:', err);
                } else {
                    console.log('File deleted successfully');
                }
            });
            
            return res.status(200).json({ message: "Route Executed Successfully!", st_data: stdout })
        });
        // return res.status(200).json({ message: "" });
    } catch (error) {
        console.error(error);
        return res.status(500).json({ error: "An error occurred while saving student details." });
    }

});


const PORT = process.env.PORT || 9999
app.listen(PORT, () => {
    console.log(`Backend listening on port ${PORT}`)
})