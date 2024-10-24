import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import "./Main.css"

import { getAccessToken } from '../../api/auth';
import Chat from "../Chat/Chat.jsx"


function markChatElemActive(id) {
    document.getElementById(id).classList.add("active");
    document.querySelectorAll(".chat").forEach((chat) => {
        if (chat.id != id) {
            chat.classList.remove("active");
        }
    });
}


function Main() {
    const [chatId, setChatId] = useState(null);
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


    const openChatHandler = (id) => {
        setChatId(id);
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
                        <div className="chat" id="1" onClick={() => openChatHandler(1)}>
                            <div className="chat-label">
                                <img src="../../../assets/user.svg" alt="" />
                                <div className="name">1</div>
                            </div>
                            {/* <div className="msg-count">3</div> */}
                        </div>
                        <div className="chat" id="2" onClick={() => openChatHandler(2)}>
                            <div className="chat-label">
                                <img src="../../../assets/user.svg" alt="" />
                                <div className="name">2</div>
                            </div>
                            {/* <div className="msg-count">10</div> */}
                        </div>
                    </div>
                </div>

                <div className="chat-window">
                    <Chat chatId={chatId} />
                </div>
            </div>
        </>
    )
}

export default Main