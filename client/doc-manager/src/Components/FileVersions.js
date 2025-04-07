import React, {useState, useEffect} from "react";
import "./../Styles/FileVersions.css"
import downloadFileAsBlob from "../Utils/DownloadFileAsBlob"

const FileVersions = () => {
    const baseUrl = process.env.REACT_APP_API_BASE_URL
    const url = `${baseUrl}/documents`
    const [fileVersions, setFileVersions] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchFileVersions = async () => {
            try {
                const token = localStorage.getItem("token");

                const response = await fetch(`${baseUrl}/api/file_versions/`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Token ${token}`,
                    },
                    credentials: "include",
                });

                if (!response.ok) {
                    throw new Error("Failed to fetch file versions");
                }

                const data = await response.json();
                setLoading(false);
                setFileVersions(data);
            } catch (err) {
                window.location = '/login';
            }
        };

        fetchFileVersions();
    }, [baseUrl]);

    const handleClick = (e) => {
        e.preventDefault();
        const token = localStorage.getItem("token");
        const fileUrl = e.target.getAttribute('href');
        const fileName = e.target.innerText.split('/').pop();
        downloadFileAsBlob(fileUrl, fileName, token);
    }

    if (loading) {
        return <p>Loading file versions...</p>;
    }

    return (
        <div className="file-versions-container">
            <h1>File Versions</h1>
            {fileVersions.length === 0 ? (
                <p>No file versions found.</p>
            ) : (
                <table className="list-of-files">
                    <thead>
                    <tr>
                        <th>File Id</th>
                        <th>Version</th>
                        <th>Path</th>
                        <th>Hash</th>
                        <th>Uploaded At</th>
                    </tr>
                    </thead>
                    <tbody>
                    {fileVersions.map((version) => (
                        <tr key={version.id}>
                            <td>{version.id}</td>
                            <td>{version.version_number}</td>
                            <td><a href={url + version.file.file_path + (version.version_number > 1 ? `?revision=${version.version_number}` : '') }
                                   onClick={handleClick}>{version.file.file_path}</a></td>
                            <td>{version.file_hash}</td>
                            <td>{new Date(version.uploaded_at).toLocaleString()}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default FileVersions;
