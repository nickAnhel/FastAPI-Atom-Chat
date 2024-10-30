import { useState, useEffect, useRef } from "react"
import "./Chat.css"

import Message from "../Message/Message";

import { getMessages } from "../../api/messages";
import { getJoinedChats } from "../../api/users";
import { joinChat, leaveChat } from "../../api/chats";


function Chat({ chatId, chatName }) {
    if (!chatId) {
        return null;
    }

    const userId = localStorage.getItem("user_id");
    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState([]);
    const [isFirstRender, setIsFirstRender] = useState(true);
    const ws = useRef(null);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scroll({
                top: messagesEndRef.current.scrollHeight,
                behavior: isFirstRender ? 'auto' : 'smooth',
            });

            setIsFirstRender(false);
        }
    }, [isFirstRender, messages]);

    useEffect(() => {
        const checkJoinedWrapper = async () => {
            const joined = await getJoinedChats(userId);
            const isJoined = joined.some((chat) => chat.chat_id === chatId);

            if (isJoined) {
                document.getElementById("chat-footer").classList.remove("hidden");
                document.getElementById("join-btn").classList.add("hidden");
            } else {
                document.getElementById("chat-footer").classList.add("hidden");
                document.getElementById("join-btn").classList.remove("hidden");
            }
        }

        checkJoinedWrapper();
    }, [userId, chatId])

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

            setIsFirstRender(true);
        }

        getMessagesWrapper();
    }, [chatId, userId]);

    useEffect(() => {
        ws.current = new WebSocket(`ws://localhost:8000/chats/${chatId}/${userId}`);

        ws.current.onmessage = (event) => {
            let data = JSON.parse(JSON.parse(event.data));
            let sender = data.user_id == userId ? "You" : data.username;
            let created_at = new Date(data.created_at + "Z");
            addMessageToChat(data.content, sender, created_at);
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

    const joinChatHandler = async () => {
        const res = await joinChat(chatId);
        if (res.ok) {
            window.location.reload();
        }
    }

    const leaveChatHandler = async () => {
        const res = await leaveChat(chatId);
        if (res.ok) {
            window.location.reload();
        }
    }

    const optionsHandler = () => {
        const button = document.getElementById('options-btn');
        const menu = document.getElementById('options');
        const rect = button.getBoundingClientRect();
        menu.style.top = `${rect.bottom + 20}px`;
        // menu.style.left = `${rect.left - 120}px`;

        menu.style.display = (menu.style.display === 'none' || menu.style.display === '') ? 'block' : 'none';
    }

    return (
        <>
            <div className="chat-header">
                <div className="header-label">
                    <img src="../../../assets/user.svg" alt="" />
                    <h2><span id="ws-id">{chatName}</span></h2>
                </div>
                <img id="options-btn" src="../../../assets/options.svg" alt="Options" onClick={optionsHandler} />
            </div>
            <div id="options">
                <div className="option leave" onClick={leaveChatHandler}>
                    <img src="../../../assets/leave.svg" alt="Leave" />
                    <div>Leave chat</div>
                </div>
            </div>

            <div className="chat-body" ref={messagesEndRef}>
                {
                    messages.map((message, index) => {
                        return (
                            <Message key={index} username={message.username} content={message.content} createdAt={message.createdAt} />
                        )
                    })
                }
            </div>

            <div id="chat-footer" className="chat-footer">
                <input type="text" placeholder="Type a message" onChange={(e) => setMessage(e.target.value)} id="message-input" onKeyDown={handleKeyDown} />
                <button onClick={sendMessage}>
                    <img src="../../../assets/send-message.svg" alt="" />
                </button>
            </div>
            <button id="join-btn" className="hidden" onClick={joinChatHandler}>Join</button>
        </>
    )
}

export default Chat