import { Routes, Route } from 'react-router-dom'
import './App.css'

import Header from './Components/Header/Header'
import Login from './Components/Login/Login'
import Register from './Components/Register/Register'
import Main from './Components/Main/Main'
import Profile from './Components/Profile/Profile'
import Restore from './Components/Restore/Restore'


function App() {

    return (
        <>
            <Header />

            <Routes>
                <Route path="/" element={<Main />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<Register />} />
                <Route path="/restore" element={<Restore />} />
                <Route path="/profile" element={<Profile />} />

            </Routes>
        </>
    )
}

export default App
