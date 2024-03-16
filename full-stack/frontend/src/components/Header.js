import React from 'react';
import { Navbar } from 'react-bootstrap';
import Container from 'react-bootstrap/Container';

const NavbarStyle = {
    backgroundColor: "lightblue",
    
};

const Header = ({title}) => {
    return (
        <Navbar style={NavbarStyle} data-bs-theme="light">
        <Container>
          <Navbar.Brand href="/">{title}</Navbar.Brand>
        </Container>
      </Navbar>
    )
};

export default Header;