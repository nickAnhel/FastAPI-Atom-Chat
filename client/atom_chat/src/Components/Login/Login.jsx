import { useState } from "react"
import { Link, useNavigate } from "react-router-dom";
import "./Login.css"

import { loginUser } from "../../api/auth";


function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const loginUserHandler = async (e) => {
        e.preventDefault();

        const success = await loginUser(username, password);
        if (!success) {
            setError('Invalid username or password');
        } else {
            setError('');
            navigate("/");
        }
    }

    return (
        <>
            <div className="login">
                <h1>Login</h1>

                <form onSubmit={loginUserHandler}>
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        minLength={1}
                        maxLength={32}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    {error && <div style={{color: 'red'}}>{error}</div>}
                    <button type="submit">Log in</button>
                    <p className="hint">
                        Don't have an account? <Link to="/signup">Sign up</Link>
                    </p>
                </form>
            </div>
        </>
    )
}

export default Login