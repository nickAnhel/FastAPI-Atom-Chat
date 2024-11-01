import "./Event.css"


function Event({ action, username, addedUserUsername }) {

    return (
        <>
            <div className="event">
                <span className="username">{username} </span>
                {action}
                <span className={addedUserUsername ? "username" : ""}> { addedUserUsername ? addedUserUsername : "chat"}</span>
            </div>
        </>
    )
}

export default Event