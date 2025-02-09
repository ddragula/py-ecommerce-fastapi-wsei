import React, { FormEvent, useState } from 'react';
import { AuthError, login, register } from '../services/auth';

const auth = { login, register}

export type AuthProps = {
    type: 'login' | 'register';
}

const Auth: React.FC<AuthProps> = ({ type }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [captcha, setCaptcha] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();

        if (!username || !password) {
            setError('Username and password are required');
            return;
        }

        if (type === 'register' && captcha !== '4') {
            setError('Captcha is wrong');
            return;
        }

        try {
            await auth[type](username, password);
            setError('');
        } catch (error) {
            const message = (error as AuthError).response?.data?.detail || (error as Error).message;
            setError(message);
        }
    }

    return (
        <div>
            <h2 className='capitalize'>{type}</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                /><br/>
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                /><br/>
                {type === 'register' && <>
                    <input
                        type="text"
                        placeholder="2 + 2 = ?"
                        value={captcha}
                        onChange={(e) => setCaptcha(e.target.value)}
                    /><br/>
                </>}
                <button type="submit" className='capitalize'>{type}</button>
            </form>
            {error && <p style={{ color: "#d00" }}>Error: {error}</p>}
        </div>
    );
};

export default Auth;