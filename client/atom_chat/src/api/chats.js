import { getAccessToken } from "./auth";



export async function createChat(title, isPrivate) {
    const token = await getAccessToken();
    const response = await fetch(
        'http://localhost:8000/chats/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            title: title,
            is_private: isPrivate,
            members: []
        })
    });
    const result = await response.json();
    return result;
}


export async function searchChats(searchText) {
    const token = await getAccessToken();
    const response = await fetch(
        `http://localhost:8000/chats/search?query=${searchText}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });
    const result = await response.json();
    return result;
}


export async function joinChat(chatId) {
    const token = await getAccessToken();
    const response = await fetch(
        `http://localhost:8000/chats/${chatId}/join`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });
    return response;
}


export async function leaveChat(chatId) {
    const token = await getAccessToken();
    const response = await fetch(
        `http://localhost:8000/chats/${chatId}/leave`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });
    return response;
}


export async function getChatHistory(chatId) {
    const token = await getAccessToken();

    const response = await fetch(
        `http://localhost:8000/chats/${chatId}/history`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });
    const result = await response.json();
    return result;
}
