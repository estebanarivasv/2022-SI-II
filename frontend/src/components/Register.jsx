import React, {useState} from "react";
import {Form, Button} from "react-bootstrap";
import "../styles/auth.css";
import {useNavigate} from "react-router-dom";
import Cookies from "universal-cookie";
import axios from "axios";

const Register = () => {
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
            await axios.post("http://localhost:5000/register", validated)
                .then((response) => {
                    if (response.status === 200) {
                        navigate("/", { replace: true });
                        window.location.reload();
                    }
                })
                .catch((err) => {
                    if (err.request.status !== 0) {
                        alert("Error");
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
                <h1>Sign Up</h1>
                <section className="auth-groups">
                    <Form.Group className="mb-3" controlId="username">
                        <Form.Label>Email address</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Enter username"
                            name="username"
                            value={validated.username}
                            onChange={handleChange}
                        />
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="password">
                        <Form.Label>Password</Form.Label>
                        <Form.Control
                            type="password"
                            placeholder="Enter password"
                            name="password"
                            value={validated.password}
                            onChange={handleChange}
                        />
                    </Form.Group>

                <Button variant="dark" className="auth-button" type="submit">
                    Sign Up
                </Button>
                <p>
                    Are you already registered? <a href="/">click here</a>
                </p>
            </section>
        </Form>
</div>
)
    ;
};

export default Register;
