import React, {useState} from "react";
import {Form, Button} from "react-bootstrap";
import "../styles/dp.css";

const SendMsg = () => {
    const [data, setData] = useState({
        username: "",
        message: ""
    });

    function handleSubmit(e) {
        e.preventDefault();

        console.log(data)
    }

    function handleChange(e) {
        const {target} = e;
        const {name, value} = target;

        const newValues = {
            ...data,
            [name]: value,
        };

        setData(newValues);
    }

    return (
        <div className="sendMsg">
            <h1>Send Message</h1>
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="username">
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Username"
                        name="username"
                        value={data.username}
                        onChange={handleChange}
                    />
                </Form.Group>
                <Form.Group className="mb-3" controlId="message">
                    <Form.Label>Message</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Message"
                        name="message"
                        value={data.message}
                        onChange={handleChange}
                    />
                </Form.Group>


                <Button variant="primary" type="submit">
                    Send
                </Button>
            </Form>
        </div>
    );
};

export default SendMsg;
