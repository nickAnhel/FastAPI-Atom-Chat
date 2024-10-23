import { getAccessToken, logoutUser } from "./auth";


export async function createUser(username, password) {
    const response = await fetch(
        'http://localhost:8000/users/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });
    const result = await response.json();
    return result;
}


export async function getProfile() {
    const token = await getAccessToken();
    const response = await fetch(
        'http://localhost:8000/users/me', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    }
    );
    const result = await response.json();
    return result;
}


export async function updateProfile(data) {
    const token = await getAccessToken();
    const response = await fetch(
        'http://localhost:8000/users/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(data)
    }
    );
    const result = await response.json();
    return result;
}


export async function deleteUser() {
    const token = await getAccessToken();
    const response = await fetch(
        'http://localhost:8000/users/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });

    const result = await response.json();

    if (response.ok) {
        await logoutUser();
    }

    return response.ok;
}