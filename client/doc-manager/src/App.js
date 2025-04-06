import './App.css';
import FileVersions from './FileVersions'

import React, {useEffect} from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from "./Components/Login";
import Logout from "./Components/Logout";
import Navigation from "./Components/Layout/Navigation";

function App() {
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
    return (
        <Router>
            <header>
                <Navigation />
            </header>
            <main>
                <Routes>
                    <Route path="/login" element={<Login/>}/>
                    <Route path="/logout" element={<Logout/>}/>
                </Routes>
            </main>
        </Router>
    );
}

export default App;
