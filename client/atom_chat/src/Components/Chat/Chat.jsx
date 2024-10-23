import { useState, useEffect } from "react"
import "./Chat.css"


const userId = localStorage.getItem("user_id");
const ws = new WebSocket(`ws://localhost:8000/chat/ws/1/${userId}`);


function Chat() {
    const [message, setMessage] = useState([])

    useEffect(() => {
        ws.onmessage = function (event) {
            let sender = event.data.split(":")[0];
            let msg = event.data.split(":").slice(1).join(":");
            addMessageToChat(msg, sender);
        };
    })

    const addMessageToChat = (msg, sender) => {
        let msgHtml;
        if (sender == "you") {
            msgHtml = `<div class="msg you"><div class="msg-label">You</div><div class="msg-text">${msg}</div></div>`;
        } else {
            msgHtml = `<div class="msg"><div class="msg-label">${sender}</div><div class="msg-text">${msg}</div></div>`;
        }

        const chatBody = document.querySelector(".chat-body");
        chatBody.innerHTML += msgHtml;
        chatBody.scrollBy({
            top: chatBody.scrollHeight,
            behavior: "smooth",
        });
    }

    const sendMessage = (event) => {
        document.getElementById("message-input").value = "";
        if (message != "") {
            addMessageToChat(message, "you");
            setMessage("");
        };
    }

    const handleKeyDown = (event) => {
        if (event.key === 'Enter' && message != "") {
            ws.send(message);
            sendMessage(message);
        }
    };

    return (
        <>

            <div className="chat-header">
                <img src="../../../assets/user.svg" alt="" />
                <h2><span id="ws-id">{userId}</span></h2>
            </div>

            <div className="chat-body"></div>

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