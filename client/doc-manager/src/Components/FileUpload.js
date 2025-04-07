import React, {useState} from "react";
import "./../Styles/FileUpload.css"

const UploadFile = () => {
    const [file, setFile] = useState(null);
    const [fileName, setFileName] = useState("");
    const [filePath, setFilePath] = useState("");
    const [uploadStatus, setUploadStatus] = useState("");
    const url = `${process.env.REACT_APP_API_BASE_URL}/api/upload/`;

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async (e) => {
        e.preventDefault()
        if (!file || !fileName || !filePath) {
            setUploadStatus("Please fill all fields and select a file before uploading.");
            return;
        }

        const token = localStorage.getItem("token");

        const formData = new FormData();
        formData.append("file", file);
        formData.append("file_name", fileName);
        formData.append("file_path", filePath);

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Authorization": `Token ${token}`,
                },
                body: formData,
            });

            if (response.ok) {
                const responseData = await response.json();
                setUploadStatus(`File uploaded successfully! Version: ${responseData.version_number}`);
            } else {
                const errorData = await response.json();
                setUploadStatus(`Upload failed: ${JSON.stringify(errorData)}`);
            }
        } catch (error) {
            console.error("Error uploading file:", error);
            setUploadStatus("An error occurred during upload.");
        }
    };

    return (
        <div className="file-upload-container">
            <h1>Upload File</h1>
            <form action={url}
                  method="post"
                  encType="multipart/form-data">
                <input
                    type="text"
                    placeholder="File Name"
                    value={fileName}
                    onChange={(e) => setFileName(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="File Path"
                    value={filePath}
                    onChange={(e) => setFilePath(e.target.value)}
                />
                <input type="file" onChange={handleFileChange}/>
                <button onClick={handleUpload}>Upload</button>
                <p>{uploadStatus}</p>
            </form>
        </div>
    );
};

export default UploadFile;
