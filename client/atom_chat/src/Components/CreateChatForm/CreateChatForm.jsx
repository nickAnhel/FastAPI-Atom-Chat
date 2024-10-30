import { useState, useEffect } from "react"
import "./CreateChatForm.css"

import { createChat } from "../../api/chats";


function CreateChatForm({ setIsCreateChatOpen }) {
    const [title, setTitle] = useState('');
    const [isPrivate, setIsPrivate] = useState(false);

    const createChatHandler = async (e) => {
        e.preventDefault();
        const result = await createChat(title, isPrivate);
        console.log(result);
        setIsCreateChatOpen(false);
        window.location.reload();
    }

    const cancelHandler = () => {
        setIsCreateChatOpen(false);
    }

    return (
        <>
            <form className="create-chat-form" onSubmit={createChatHandler}>
                <h2>Create Chat</h2>
                <input
                    id="title"
                    type="text"
                    placeholder="Title"
                    value={title}
                    onChange={e => setTitle(e.target.value)}
                />

                <div className="item">
                    <input
                        id="isPrivate"
                        type="checkbox"
                        // checked={isPrivate}
                        onChange={e => setIsPrivate(e.target.checked)}
                    />
                    <label htmlFor="isPrivate">Private</label>
                </div>


                <button type="submit">Create</button>
                <button className="cancel" onClick={cancelHandler}>Cancel</button>
            </form>
        </>
    )
}

export default CreateChatForm