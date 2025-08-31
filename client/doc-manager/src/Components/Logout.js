import {useNavigate} from "react-router";

const Logout = () => {
    const navigate = useNavigate();
    localStorage.removeItem('token')
    window.location = '/login';
};

export default Logout;
