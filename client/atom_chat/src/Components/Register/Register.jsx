import { useState } from "react"
import { useNavigate } from "react-router-dom";
import { createUser } from "../../api/users";
import { loginUser } from "../../api/auth";
import "./Register.css"


function Register() {
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState('');

    const registerUserHandler = async (e) => {
        e.preventDefault();
        const result = await createUser(username, password);
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
            <div className="register">
                <h1>Sign Up</h1>

                <form onSubmit={registerUserHandler}>
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

export default Register