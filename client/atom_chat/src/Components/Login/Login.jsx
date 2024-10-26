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

        const status = await loginUser(username, password);

        switch (status) {
            case 401:
                setError('Invalid username or password');
                break;
            case 410:
                setError('This account has been deleted');
                break;
            case 403:
                setError('This account has been blocked');
                break;
            default:
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

                    <div className="hints">
                        <p className="hint">
                            Don't have an account? <Link to="/signup">Sign up</Link>
                        </p>
                        <p className="hint">
                            Want to restore deleted account? <Link to="/restore">Restore</Link>
                        </p>
                    </div>
                </form>
            </div>
        </>
    )
}

export default Login