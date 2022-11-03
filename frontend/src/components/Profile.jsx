import React, {useEffect} from "react";
import "../styles/dp.css";
import Cookies from "universal-cookie";
import axios from "axios";
import {Table} from "react-bootstrap";

const Profile = () => {
    const cookies = new Cookies();
    const headers = {
        "content-type": "application/json",
        Authorization: "Bearer " + cookies.get("token"),
    };
    let i = 1;
    const [messages, setMessages] = React.useState([]);

    async function handleData() {
        await axios
            .get("http://localhost:5000/profile", {headers})
            .then(async (response) => {
                if (response.status === 200) {
                    console.log(response.data);
                    setMessages(response.data.messages);
                }
            });
    }

    useEffect(() => {
        handleData();
    }, []);

    return (
        <div className="sendMsg">
            <h1 className="titleProfile">Lista de correos de {cookies.get("username")}</h1>
            <div style={{marginTop: "50px" ,fontSize: "25px", width: "90%"}}>
                <Table striped bordered hover>
                    <thead>
                    <tr>
                        <th>#</th>
                        <th>Message</th>
                        <th>Sender</th>
                        <th>Date</th>
                    </tr>
                    </thead>

                    <tbody>
                    {messages.map((message) => (
                        <tr>
                            <td>{i++}</td>
                            <td>{message.text}</td>
                            <td>{message.sender}</td>
                            <td>{message.date}</td>
                        </tr>
                    ))}
                    </tbody>
                </Table>
            </div>

        </div>
    );
};

export default Profile;
