import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import "./Main.css"

import { getAccessToken } from '../../api/auth';
import { getJoinedChats } from "../../api/users.js";
import { searchChats, createChat } from "../../api/chats.js";

import Chat from "../Chat/Chat.jsx"
import ChatListItem from "../ChatListItem/ChatListItem.jsx";
import CreateChatForm from "../CreateChatForm/CreateChatForm.jsx";


function Main() {
    const userId = localStorage.getItem("user_id");
    const [chats, setChats] = useState([]);
    const [chatId, setChatId] = useState(null);
    const [chatName, setChatName] = useState(null);
    const [searchQuery, setSearchQuery] = useState("");
    const [isCreateChatOpen, setIsCreateChatOpen] = useState(false);
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
        loadJoinedChats();
    }, [userId]);

    const markChatElemActive = (id) => {
        document.getElementById(id).classList.add("active");
        document.querySelectorAll(".chat").forEach((chat) => {
            if (chat.id != id) {
                chat.classList.remove("active");
            }
        });
    }

    const loadJoinedChats = async () => {
        clearChatList();
        const chats = await getJoinedChats(userId);
        chats.forEach(
            (chat) => {
                addChatToList(chat);
            }
        );
    }

    const clearChatList = () => {
        setChats([]);
    }

    const addChatToList = (chat) => {
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

    const handleKeyDown = (event) => {
        if (event.key === 'Enter' && searchQuery != "") {
            search();
        } else if (event.key === 'Escape') {
            clearSearch();
        }
    };

    const clearSearch = () => {
        setSearchQuery("");
        document.getElementById("search-input").value = "";
        document.getElementById("clear-search-btn").classList.add("hidden");
        document.getElementById("search-btn").classList.remove("hidden");
        document.getElementById("create-chat").style.display = "flex";
        loadJoinedChats();
    }

    const search = async () => {
        if (searchQuery == "") {
            return;
        }

        document.getElementById("search-btn").classList.add("hidden");
        document.getElementById("clear-search-btn").classList.remove("hidden");
        document.getElementById("create-chat").style.display = "none";

        clearChatList();

        const chats = await searchChats(searchQuery);
        chats.forEach(
            (chat) => {
                addChatToList(chat);
            }
        );
    }

    const createChatHandler = async () => {
        setIsCreateChatOpen(true);
    }

    return (
        <>
            <div className="chat-container">
                <div className="chat-list">
                    <div className="search">
                        <input id="search-input" type="text" placeholder="Search" onChange={(e) => setSearchQuery(e.target.value)} onKeyDown={handleKeyDown}/>
                        <button id="search-btn" onClick={() => search()}>
                            <img src="../../../assets/search.svg" alt="" />
                        </button>
                        <button id="clear-search-btn" onClick={() => clearSearch()} className="hidden">
                            <img src="../../../assets/clear.svg" alt="" />
                        </button>
                    </div>

                    <div className="chats">
                        <div id="create-chat" className="chat create" onClick={createChatHandler}>
                            <div className="chat-label">
                                <img src="../../../assets/plus.svg" alt="" />
                                <div className="name">Create new chat</div>
                            </div>
                        </div>

                        { isCreateChatOpen ? <div></div> :
                            chats.map((chat, index) => {
                                return (
                                    <ChatListItem key={index} chatId={chat.chatId} chatName={chat.chatName} onClickHandler={openChatHandler}/>
                                )
                            })
                        }
                    </div>
                </div>

                <div className="chat-window">
                    {
                        isCreateChatOpen ?
                        <CreateChatForm setIsCreateChatOpen={setIsCreateChatOpen} /> :
                        <Chat chatId={chatId} chatName={chatName} />
                    }
                </div>
            </div>
        </>
    )
}

export default Main