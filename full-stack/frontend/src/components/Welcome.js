import React from 'react';
import { Button } from 'react-bootstrap';

const Welcome = () => (
  <div className="bg-light p-5 rounded-lg m-3">
    <h1 className="display-4">Images Gallery</h1>
    <p className="lead">
      This is a simple application that retrieves photos from the Unsplash API.
      In order to start, enter any search term in the input field.{' '}
    </p>
    <p>
      <Button variant="primary" href="https://unsplash.com" target="_blank">
        Learn more
      </Button>
    </p>
  </div>
);

export default Welcome;
