import {Link} from "react-router-dom";
import React, {useEffect, useState} from "react";
import './../../Styles/Navigation.css';

function Navigation() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem("token");
        setIsAuthenticated(!!token)
    }, []);

    return (
        <nav>
            <ul>
                {isAuthenticated && <li><Link to="/">List of files</Link></li>}
                {isAuthenticated && <li><Link to="/upload">Upload File</Link></li>}
                {isAuthenticated && <li><Link to="/logout">Logout</Link></li>}
                {!isAuthenticated && <li><Link to="/login">Login</Link></li>}
            </ul>
        </nav>
    )
}

export default Navigation;
