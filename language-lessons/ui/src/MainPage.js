import React, { useState } from 'react';
import SupportPanel from './components/SupportElements.js'

function MainPage() {

    return (
      <div className="mx-auto bg-gray-200 rounded-xl shadow border p-10 flex">
          <SupportPanel></SupportPanel>      
      </div>
    );
  }
  
  export default MainPage;
  