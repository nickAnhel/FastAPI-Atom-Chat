import { useState } from "react"
import { useNavigate } from "react-router-dom";
import { restoreUser } from "../../api/users";
import { loginUser } from "../../api/auth";
import "./Restore.css"


function Restore() {
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState('');

    const restoreUserHandler = async (e) => {
        e.preventDefault();
        const result = await restoreUser(username, password);
        if (result?.detail) {
            console.log(result);
            setError(result.detail);
        } else {
            await loginUser(username, password);
            navigate("/");
        }
    }

    return (
        <>
            <div className="restore">
                <h1>Restore account</h1>

                <form onSubmit={restoreUserHandler}>
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={e => setUsername(e.target.value)}
                        minLength={1}
                        maxLength={32}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        required
                    />
                    {error && <div className="error">{error}</div>}
                    <button type="submit">Sign Up</button>
                </form>
            </div>
        </>
    )
}

export default Restore