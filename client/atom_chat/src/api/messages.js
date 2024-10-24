import { getAccessToken } from "./auth";


export async function  getMessages(chatId) {
    const token = await getAccessToken();

    const response = await fetch(
        `http://localhost:8000/chat/${chatId}/messages`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });
    const result = await response.json();
    return result;
}