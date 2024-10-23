import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import "./Main.css"

import { getAccessToken } from '../../api/auth';
import Chat from "../Chat/Chat.jsx"


function Main() {
    const [chatId, setChatId] = useState(1);
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
                        <div className="chat">
                            <div className="chat-label">
                                <img src="../../../assets/user.svg" alt="" />
                                <div className="name">John</div>
                            </div>
                            <div className="msg-count">3</div>
                        </div>
                        <div className="chat active">
                            <div className="chat-label">
                                <img src="../../../assets/user.svg" alt="" />
                                <div className="name">Linda</div>
                            </div>
                            <div className="msg-count">10</div>
                        </div>
                        <div className="chat">
                            <div className="chat-label">
                                <img src="../../../assets/user.svg" alt="" />
                                <div className="name">Bob</div>
                            </div>
                            {/* <div className="msg-count"></div> */}
                        </div>

                    </div>
                </div>

                <div className="chat-window">
                    <Chat />
                </div>
            </div>
        </>
    )
}

export default Main