import api from './api';

export interface AuthError {
    response?: {
        data?: {
            detail: string;
        }
    }
}

type LoginListenerCallback = (username: string|null) => void;

const loginListeners: Map<string, LoginListenerCallback> = new Map();

export function addLoginListener(key: string, callback: LoginListenerCallback) {
    loginListeners.set(key, callback);
}

export function getUsername() {
    return localStorage.getItem('username');
}

export function getToken() {
    return localStorage.getItem('token');
}

export async function login(username: string, password: string) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const resp = await api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });

    localStorage.setItem('username', username);
    localStorage.setItem('token', resp.data.access_token);

    loginListeners.forEach((callback) => callback(username));

    return resp;
}

export async function register(username: string, password: string) {
    return await api.post('/auth/register', { username, password});
}

export function logout() {
    localStorage.removeItem('username');
    localStorage.removeItem('token');

    loginListeners.forEach((callback) => callback(null));
}
