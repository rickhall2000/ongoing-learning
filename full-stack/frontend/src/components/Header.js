import React from 'react';
import { Navbar } from 'react-bootstrap';
import Container from 'react-bootstrap/Container';
import { ReactComponent as Logo } from '../images/logo.svg';

const NavbarStyle = {
  backgroundColor: '#eeeeee',
};

const Header = ({ title }) => {
  return (
    <Navbar style={NavbarStyle} data-bs-theme="light">
      <Container>
        <Logo alt={title} style={{ maxWidth: '12rem', maxHeight: '2rem' }} />
      </Container>
    </Navbar>
  );
};

export default Header;
