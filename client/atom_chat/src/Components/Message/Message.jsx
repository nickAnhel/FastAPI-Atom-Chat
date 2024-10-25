import { useEffect } from "react"
import "./Message.css"


function Message({ username, content, createdAt }) {
    const createdAtTimeLocal = new Date(createdAt).toLocaleTimeString().split(":").slice(0, 2).join(":");

    return (
        <>
            <div className={username == "You" ? "msg you" : "msg"}>
                <div className="msg-label">
                    <div className="username">{username}</div>
                    <div>{createdAtTimeLocal}</div>
                </div>
                <div className="msg-text">{content}</div>
            </div>
        </>
    )
}

export default Message