import { isTokenExpired } from "../utils/jwt";
import { getProfile } from "./users";
import { clearStorage } from "./storage";


export async function loginUser(username, password) {
    const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `grand_type=password&username=${username}&password=${password}`,
    });
    const data = await response.json();
    if (response.ok) {
        localStorage.setItem('access_token', data.access_token);
    }

    let userData = await getProfile();
    if (userData) {
        localStorage.setItem('user_id', userData.user_id);
    }

    return response.ok;
}


export async function getAccessToken() {
    let token = localStorage.getItem('access_token');

    if (isTokenExpired(token)) {
        token = await getNewAccessToken();
    }

    return token;
}


export async function getNewAccessToken() {
    const response = await fetch('http://localhost:8000/auth/new-access-token', {
        method: 'POST',
        credentials: 'include',
    });
    const data = await response.json();
    if (response.ok) {
        localStorage.setItem('access_token', data.access_token);
        return data.access_token;
    } else {
        // window.location.href = '/login';
        // return <Redirect to={"/login"} />;
    }
}


export async function logoutUser() {
    clearStorage();
    const response = await fetch(
        'http://localhost:8000/auth/logout', {
        method: 'POST',
        credentials: 'include',
    }
    );
}