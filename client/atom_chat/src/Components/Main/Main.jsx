import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import "./Main.css"

import { getAccessToken } from '../../api/auth';
import { getJoinedChats } from "../../api/users.js";

import Chat from "../Chat/Chat.jsx"
import ChatListItem from "../ChatListItem/ChatListItem.jsx";


function markChatElemActive(id) {
    document.getElementById(id).classList.add("active");
    document.querySelectorAll(".chat").forEach((chat) => {
        if (chat.id != id) {
            chat.classList.remove("active");
        }
    });
}


function Main() {
    const userId = localStorage.getItem("user_id");
    const [chats, setChats] = useState([]);
    const [chatId, setChatId] = useState(null);
    const [chatName, setChatName] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const setIsLoggedInWrapper = async () => {
            const token = await getAccessToken();
            if (!token) {
                navigate("/login");
            }
        };

        setIsLoggedInWrapper();
    }, []);

    useEffect(() => {
        const getChatsWrapper = async () => {
            clearChatList();

            const chats = await getJoinedChats(userId);
            chats.forEach(
                (chat) => {
                    addChatToList(chat);
                }
            );
        }

        getChatsWrapper();
    }, [userId]);

    const clearChatList = () => {
        setChats([]);
    }

    const addChatToList = (chat) => {
        console.log(chat);
        setChats(chats => [...chats, {
            chatId: chat.chat_id,
            chatName: chat.title,
        }]);
    }

    const openChatHandler = (id, name) => {
        setChatId(id);
        setChatName(name)
        markChatElemActive(id);
    }

    return (
        <>
            <div className="chat-container">
                <div className="chat-list">
                    <div className="search">
                        <input type="text" placeholder="Search" />
                        <button>
                            <img src="../../../assets/search.svg" alt="" />
                        </button>
                    </div>

                    <div className="chats">
                        {
                            chats.map((chat, index) => {
                                return (
                                    <ChatListItem key={index} chatId={chat.chatId} chatName={chat.chatName} onClickHandler={openChatHandler}/>
                                )
                            })
                        }
                    </div>
                </div>

                <div className="chat-window">
                    <Chat chatId={chatId} chatName={chatName} />
                </div>
            </div>
        </>
    )
}

export default Main