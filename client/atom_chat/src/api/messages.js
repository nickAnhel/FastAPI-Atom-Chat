import { getAccessToken } from "./auth";


export async function  getChatMessages(chatId) {
    const token = await getAccessToken();

    const response = await fetch(
        `http://localhost:8000/messages/?chat_id=${chatId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });
    const result = await response.json();
    return result;
}