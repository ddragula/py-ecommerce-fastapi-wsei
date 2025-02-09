import React, { useEffect } from 'react';
import { addLoginListener, getUsername, logout } from '../../services/auth';
import { useNavigate } from 'react-router-dom';
import './Header.css';

export const Header: React.FC = () => {
    const [username, setUsername] = React.useState<string | null>(getUsername());
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/');
    }

    useEffect(() => {
        addLoginListener('Header', setUsername);
    }, []);

    const loggedContent = <>
        <p>Welcome, {username}</p>
        <div className="grow"></div>
        <button onClick={() => navigate('/basket')}>Basket</button>
        <button onClick={() => navigate('/orders')}>My Orders</button>
        <button onClick={() => handleLogout()}>Log out</button>
    </>;

    const notLoggedContent = <>
        <p>Please log in or register</p>
        <div className="grow"></div>
        <button onClick={() => navigate('/login')}>Log in</button>
        <button onClick={() => navigate('/register')}>Register</button>
    </>;

    return (
        <div className="Header-container">
            {username ? loggedContent : notLoggedContent}
            <button onClick={() => navigate('/')}>Main Page</button>
        </div>
    );
}
