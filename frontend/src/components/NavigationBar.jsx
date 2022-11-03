import React from "react";
import {Navbar, Nav, Container} from "react-bootstrap";

const NavigationBar = () => {
    return (
        <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
            <Container>
                <Navbar.Brand href="/profile" style={{fontSize: "20px", marginRight: "70%"}}>
                    WEB
                </Navbar.Brand>

                <Navbar.Toggle aria-controls="responsive-navbar-nav"/>
                <Navbar.Collapse id="responsive-navbar-nav">

                    <Nav>
                        <Nav.Link href="/send">Send Message</Nav.Link>
                        <Nav.Link href="/">Sign Out</Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
};

export default NavigationBar;
