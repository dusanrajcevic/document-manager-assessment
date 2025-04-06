import './App.css';
import FileVersions from './FileVersions'

import React, {useEffect} from 'react';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <FileVersions />
      </header>
    </div>
  );
    // Fetch the CSRF token when the app loads
    useEffect(() => {
        const fetchCsrfToken = async () => {
            let response = await fetch("http://127.0.0.1:8001/api-auth/login/", {
                method: "GET",
                credentials: "include", // Include cookies
            });
        };

        fetchCsrfToken();
    }, []);
}

export default App;
