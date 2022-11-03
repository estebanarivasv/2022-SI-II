import React from "react";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import "./App.css";
import Login from "./components/Login";
import Register from "./components/Register";
import NavigationBar from "./components/NavigationBar";
import Profile from "./components/Profile";
import SendMsg from "./components/SendMsg";

function App() {
    return (
        <div>
            <BrowserRouter>
                <NavigationBar/>
                <Routes>
                    <Route path="/" element={<Login/>}/>
                    <Route path="/register" element={<Register/>}/>
                    <Route path="/profile" element={<Profile/>}/>
                    <Route path="/send" element={<SendMsg/>}/>
                </Routes>
            </BrowserRouter>
        </div>
    );
}

export default App;
