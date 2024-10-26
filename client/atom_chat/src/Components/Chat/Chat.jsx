import { useState, useEffect, useRef } from "react"
import { getMessages } from "../../api/messages";
import "./Chat.css"

import Message from "../Message/Message";




function Chat({ chatId }) {
    if (!chatId) {
        return null;
    }

    const userId = localStorage.getItem("user_id");
    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState([]);
    const ws = useRef(null);
    const messagesEndRef = useRef(null);


    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scroll({
                top: messagesEndRef.current.scrollHeight,
                behavior: 'smooth'
            });
        }
    }, [messages]);

    useEffect(() => {
        const getMessagesWrapper = async () => {
            clearChat();

            const msgs = await getMessages(chatId);
            msgs.reverse().forEach(
                (message) => {
                    let sender = message.user_id == userId ? "You" : message.user.username;
                    let created_at = new Date(message.created_at + "Z");
                    addMessageToChat(message.content, sender, created_at);
                }
            );
        }

        getMessagesWrapper();
    }, [chatId, userId]);

    useEffect(() => {
        ws.current = new WebSocket(`ws://localhost:8000/chat/ws/${chatId}/${userId}`);

        ws.current.onmessage = (event) => {
            let data = JSON.parse(JSON.parse(event.data));
            let sender = data.user_id == userId ? "You" : message.user.username;
            addMessageToChat(data.content, sender, data.created_at);
        };

        return () => {
            ws.current.close();
        };
    }, [chatId, userId]);

    const clearChat = () => {
        setMessages([]);
    }

    const addMessageToChat = (msg, sender, createdAt) => {
        setMessages(messages => [...messages, {
            content: msg,
            username: sender,
            createdAt: createdAt
        }]);
    }

    const sendMessage = (event) => {
        document.getElementById("message-input").value = "";
        if (message != "") {
            let now = new Date();
            addMessageToChat(message, "You", now);

            let msgData = {
                content: message,
                created_at: new Date()
            }
            ws.current.send(
                JSON.stringify(msgData)
            );
            setMessage("");
        };
    }

    const handleKeyDown = (event) => {
        if (event.key === 'Enter' && message != "") {
            sendMessage(message);
        }
    };

    return (
        <>

            <div className="chat-header">
                <img src="../../../assets/user.svg" alt="" />
                <h2><span id="ws-id">{chatId}</span></h2>
            </div>

            <div className="chat-body" ref={messagesEndRef}>
                {
                    messages.map((message, index) => {
                        return (
                            <Message key={index} username={message.username} content={message.content} createdAt={message.createdAt}/>
                        )
                    })
                }
            </div>

            <div className="chat-footer">
                <input type="text" placeholder="Type a message" onChange={(e) => setMessage(e.target.value)} id="message-input" onKeyDown={handleKeyDown} />
                <button onClick={sendMessage}>
                    <img src="../../../assets/send-message.svg" alt="" />
                </button>
            </div>
        </>
    )
}

export default Chat