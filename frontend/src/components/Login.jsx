import React, {useState} from "react";
import "../styles/auth.css";

import {Form, Button} from "react-bootstrap";

const Login = () => {
    const [validated, setValidated] = useState({
        username: '',
        password: '',
    });

    function handleSubmit(e) {
        e.preventDefault();
        console.log(validated)
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
                        <Form.Label> Email address < /Form.Label>
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