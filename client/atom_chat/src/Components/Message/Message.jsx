import { useEffect } from "react"
import "./Message.css"


function Message({ username, content, createdAt }) {
    const createdAtPretty = new Date(createdAt).toTimeString().split(" ")[0].split(":").slice(0, 2).join(":");

    return (
        <>
            <div className={username == "You" ? "msg you" : "msg"}>
                <div className="msg-label">
                    <div>{username}</div>
                    <div>{createdAtPretty}</div>
                </div>
                <div className="msg-text">{content}</div>
            </div>
        </>
    )
}

export default Message