import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import "./ChatListItem.css"

import { getAccessToken } from '../../api/auth';
import Chat from "../Chat/Chat.jsx"



function ChatListItem({ chatId, chatName, onClickHandler }) {
    return (
        <>
            <div className="chat" id={chatId} onClick={() => onClickHandler(chatId, chatName)}>
                <div className="chat-label">
                    <img src="../../../assets/user.svg" alt="" />
                    <div className="name">{chatName}</div>
                </div>
            </div>
        </>
    )
}

export default ChatListItem