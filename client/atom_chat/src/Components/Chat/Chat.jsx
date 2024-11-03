import { useState, useEffect, useRef } from "react"
import { io } from "socket.io-client";
import "./Chat.css"

import Message from "../Message/Message";
import Event from "../Event/Event";

import { getJoinedChats } from "../../api/users";
import { joinChat, leaveChat, getChatHistory } from "../../api/chats";


function getMaxCharsInLine(textarea, content) {
    const context = document.createElement('canvas').getContext('2d');
    const computedStyle = window.getComputedStyle(textarea);
    context.font = computedStyle.font;
    const width = context.measureText(content).width / content.length;
    return Math.floor(textarea.clientWidth / width);
}


function Chat({ chatId, chatName }) {
    if (!chatId) {
        return null;
    }

    const userId = localStorage.getItem("user_id");
    const [chatItems, setChatItems] = useState([]);
    const [message, setMessage] = useState([]);
    const [isFirstRender, setIsFirstRender] = useState(true);
    const socket = useRef(null);
    const messagesEndRef = useRef(null);
    const textareaRef = useRef(null);

    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scroll({
                top: messagesEndRef.current.scrollHeight,
                behavior: isFirstRender ? 'auto' : 'smooth',
            });

            setIsFirstRender(false);
        }
    }, [isFirstRender, chatItems]);

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
        const getHistoryWrapper = async () => {
            clearChat();

            const items = await getChatHistory(chatId);

            items.forEach(
                (item) => {
                    if (item.item_type == "message") {
                        let sender = item.user_id == userId ? "You" : item.user.username;
                        addMessageToChat(item.content, sender, item.created_at);
                    } else if (item.item_type == "event") {
                        switch (item.event_type) {
                            case "joined":
                                addEventToChat(item.event_type, item.user.username, null);
                                break;
                            case "leaved":
                                addEventToChat(item.event_type, item.user.username, null);
                                break;
                            case "created":
                                addEventToChat(item.event_type, item.user.username, null);
                                break;
                            case "added":
                                addEventToChat(item.event_type, item.user.username, item.altered_user.username);
                                break;
                            case "removed":
                                addEventToChat(item.event_type, item.user.username, item.altered_user.username);
                                break;
                        }
                    }

                }
            );

            setIsFirstRender(true);
        }

        getHistoryWrapper();
    }, [chatId, userId]);

    useEffect(() => {
        socket.current = io("ws://localhost:8000", {
            path: "/ws",
            transports: ["websocket"],
            upgrade: false,
        });

        socket.current.emit("join", {
            chat_id: chatId,
        })

        socket.current.on("message", (data) => {
            let msgData = JSON.parse(data);
            let sender = msgData.user_id == userId ? "You" : msgData.username;
            addMessageToChat(msgData.content, sender, msgData.created_at);
        })

        return () => {
            socket.current.emit("leave", {
                chat_id: chatId,
            });
        }
    }, [chatId, userId]);

    const resizeTextarea = () => {
        let rowsTotalHeight = textareaRef.current.value.split("\n").length * 25;
        let symbolsTotalLength = Math.max(
            Math.ceil(textareaRef.current.value.length / getMaxCharsInLine(textareaRef.current, textareaRef.current.value)), 1
        ) * 25;

        textareaRef.current.style.height = `${Math.min(
            symbolsTotalLength ? Math.max(rowsTotalHeight, symbolsTotalLength) : rowsTotalHeight,
            200
        )
            }px`;

        messagesEndRef.current.scroll({
            top: messagesEndRef.current.scrollHeight,
            behavior: 'smooth',
        });
    }

    const clearChat = () => {
        setChatItems([]);
    }

    const addMessageToChat = (msg, sender, createdAt) => {
        setChatItems(items => [...items, {
            type: "message",
            content: msg,
            username: sender,
            createdAt: createdAt
        }]);
    }

    const addEventToChat = (action, username, addedUserUsername) => {
        setChatItems(items => [...items, {
            type: "event",
            action: action,
            username: username,
            addedUserUsername: addedUserUsername
        }]);
    }

    const sendMessage = (event) => {
        if (message.trim() != "") {
            document.getElementById("message-input").value = "";

            let now = new Date();
            addMessageToChat(message.trim(), "You", now);

            let msgData = {
                chat_id: chatId,
                user_id: userId,
                content: message.trim(),
                created_at: new Date()
            }

            socket.current.emit("message", msgData);

            setMessage("");
            textareaRef.current.value = "";
        } else {
            textareaRef.current.focus()
        }
    }

    const handleKeyDown = (event) => {
        if (event.shiftKey && event.key === 'Enter' && message.trim() != "") {
            return;
        }
        else if (event.key === 'Enter' && message.trim() != "") {
            sendMessage(message);
            event.preventDefault();
            resizeTextarea();
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
                    chatItems.map((item, index) => {
                        if (item.type == "message") {
                            return (
                                <Message key={index} username={item.username} content={item.content} createdAt={item.createdAt} />
                            )
                        } else if (item.type == "event") {
                            return (
                                <Event key={index} action={item.action} username={item.username} addedUserUsername={item.addedUserUsername} />
                            )
                        }
                    })
                }
            </div>

            <div id="chat-footer" className="chat-footer">
                {/* <input type="text" placeholder="Type a message" onChange={(e) => setMessage(e.target.value)} id="message-input" onKeyDown={handleKeyDown} /> */}
                <div className="msg-box">
                    <textarea
                        name="message-input"
                        ref={textareaRef}
                        value={message}
                        placeholder="Type a message"
                        onChange={(e) => { setMessage(e.target.value); resizeTextarea() }}
                        id="message-input"
                        onKeyDown={handleKeyDown}
                    >
                    </textarea>
                </div>
                <button onClick={sendMessage}>
                    <img src="../../../assets/send-message.svg" alt="" />
                </button>
            </div>
            <button id="join-btn" className="hidden" onClick={joinChatHandler}>Join</button>
        </>
    )
}

export default Chat