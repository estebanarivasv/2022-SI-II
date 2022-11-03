import React, {useState} from "react";
import {Form, Button} from "react-bootstrap";
import "../styles/dp.css";
import axios from "axios";
import Cookies from "universal-cookie";
import {useNavigate} from "react-router-dom";

const SendMsg = () => {
    const [data, setData] = useState({
        receiver: "",
        text: ""
    });

    const navigate = useNavigate();
    const cookies = new Cookies();

    async function handleSubmit(e) {
        e.preventDefault();
        if (!(data.receiver === "") && !(data.text === "")) {
            await axios.post("http://localhost:5000/sendmail", data, {
                headers: {
                    "Authorization": "Bearer " + cookies.get("token")
                }
            }).then((response) => {
                if (response.status === 200) {
                    navigate("/profile", {replace: true});
                    window.location.reload();
                }
            }).catch((err) => {
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
            ...data,
            [name]: value,
        };

        setData(newValues);
    }

    return (
        <div className="sendMsg">
            <h1>Send Message</h1>
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="receiver">
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Username"
                        name="receiver"
                        value={data.receiver}
                        onChange={handleChange}
                    />
                </Form.Group>
                <Form.Group className="mb-3" controlId="text">
                    <Form.Label>Message</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Message"
                        name="text"
                        value={data.text}
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
