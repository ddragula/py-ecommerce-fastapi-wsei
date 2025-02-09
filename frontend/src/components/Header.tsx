import React, { useEffect } from 'react';
import { addLoginListener, getUsername, logout } from '../services/auth';
import { useNavigate } from 'react-router-dom';

export const Header: React.FC = () => {
    const [username, setUsername] = React.useState<string | null>(getUsername());
    const navigate = useNavigate();

    useEffect(() => {
        addLoginListener('Header', setUsername);
    }, []);

    const loggedContent = <>
        <p>Welcome, {username}</p>
        <button onClick={() => logout()}>Log out</button>
    </>;

    const notLoggedContent = <>
        <p>Please log in</p>
        <button onClick={() => navigate('/login')}>Log in</button>
        <button onClick={() => navigate('/register')}>Register</button>
    </>;

    return (
        <div className="header">
            {username ? loggedContent : notLoggedContent}
        </div>
    );
}
