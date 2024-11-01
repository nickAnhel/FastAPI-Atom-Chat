import { useEffect } from "react"
import "./Event.css"


function Event({ action, username }) {
    return (
        <>
            <div className="event">
                <span className="username">{username} </span> {action} chat
            </div>
        </>
    )
}

export default Event