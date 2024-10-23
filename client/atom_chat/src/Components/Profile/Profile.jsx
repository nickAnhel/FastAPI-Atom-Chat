import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { Popup } from "reactjs-popup"
import "./Profile.css"

import { getProfile, updateProfile, deleteUser } from "../../api/users"
import { logoutUser } from "../../api/auth"


function Profile() {
    const [username, setUsername] = useState("");
    const [error, setError] = useState('');

    const navigate = useNavigate();

    useEffect(() => {
        const getProfileAndSetUsername = async () => {
            const profileData = await getProfile();
            setUsername(profileData.username);
        };

        getProfileAndSetUsername();
    }, []);

    const updateProfileHandler = async (event) => {
        event.preventDefault();

        if (!username) {
            setError("Username can't be empty");
            return;
        }

        const result = await updateProfile({
            username: username
        });
        console.log(result);

        if (result.detail?.[0].msg) {
            setError(result.detail[0].msg);
        } else if (result.detail) {
            setError(result.detail);
        } else {
            window.location.reload();
        }
    }

    const deleteUserHandler = async (event) => {
        const success = await deleteUser();
        if (!success) {
            setError('Failed to delete account');
        } else {
            setError('');
            navigate("/login");
        }
    }

    const logoutHandler = async (event) => {
        await logoutUser();
        navigate("/login");
    }

    return (
        <>
            <div className="profile">
                <img src="../../../assets/user.svg" alt="" />

                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    minLength={1}
                    maxLength={32}
                    required
                />

                {error && <div className="error">{error}</div>}
                <button onClick={updateProfileHandler} className="save">Save Changes</button>

                <Popup trigger=
                    {<button className="delete"> Delete account </button>}
                    modal nested>
                    {
                        close => (
                            <div className='modal'>
                                <div className="modal-body">
                                    <div className='content'>
                                        Are you sure you want to delete your account?
                                    </div>
                                    <button onClick={() => {deleteUserHandler(); close()}} className="delete">
                                        Delete
                                    </button>
                                </div>
                            </div>
                        )
                    }
                </Popup>

                <button onClick={logoutHandler} className="logout">Logout</button>
            </div>
        </>
    )
}

export default Profile