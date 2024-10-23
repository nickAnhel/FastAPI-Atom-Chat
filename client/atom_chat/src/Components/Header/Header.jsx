import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import './Header.css'

import { getAccessToken } from '../../api/auth';


function Header() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        const setIsLoggedInWrapper = async () => {
            const token = await getAccessToken();
            setIsLoggedIn(!!token);
        };

        setIsLoggedInWrapper();
    }, []);

    return (
        <>
            <div className="header">
                <div className='logo'><Link to="/">Atom Chat</Link></div>
                <div className='navbar'>
                    {isLoggedIn ? <Link to="/profile">Profile</Link> : <Link to="/login">Login</Link>}
                </div>
            </div>
        </>
    )
}

export default Header