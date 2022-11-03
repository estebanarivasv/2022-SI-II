import React, {useState} from "react";
import "../styles/auth.css";

import axios from "axios";
import Cookies from "universal-cookie";
import { useNavigate } from "react-router-dom";
import {Form, Button} from "react-bootstrap";

const Login = () => {
    const [validated, setValidated] = useState({
        username: '',
        password: '',
    });

    const navigate = useNavigate();
    const cookies = new Cookies();
    cookies.remove("token");
    cookies.remove("username");

    async function handleSubmit(e) {
        e.preventDefault();
        if (!(validated.username === "") && !(validated.password === "")) {
            await axios.post("http://localhost:5000/login", validated)
                .then((response) => {
                    if (response.status === 200) {
                        cookies.set("token", response.data.access_token, {path: "/"});
                        cookies.set("username", validated.username);
                        navigate("/profile", { replace: true });
                        window.location.reload();
                    }
                })
                .catch((err) => {
                    if (err.request.status !== 0) {
                        alert("Wrong username or password");
                    }
                });
        }
    }

    function handleChange(e) {
        const {target} = e;
        const {name, value} = target;

        const newValues = {
            ...validated,
            [name]: value,
        };

        setValidated(newValues);
    }


    return (
        <div className="auth">
            <Form className="auth-form" onSubmit={handleSubmit}>
                <h1> Sign In </h1>
                <section className="auth-groups">
                    <Form.Group className="mb-3" controlId="formBasicEmail">
                        <Form.Label> Username < /Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Enter username"
                            name="username"
                            value={validated.username}
                            onChange={handleChange}
                        />
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formBasicPassword">
                        <Form.Label> Password < /Form.Label>
                        <Form.Control
                            type="password"
                            placeholder="Enter password"
                            name="password"
                            value={validated.password}
                            onChange={handleChange}
                        />
                    </Form.Group>
                    <Button variant="dark" className="auth-button" type="submit">
                        Sign In
                    </Button>
                    <p>
                        You are not registered ? < a href="/register"> click here < /a>
                    </p>
                </section>
            </Form>
        </div>
    );
};

export default Login;