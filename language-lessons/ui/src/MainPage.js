import React, { useState } from 'react';
import SupportPanel from './components/SupportElements.js'
import ConversationUI from './components/ConversationUI.js'

function MainPage() {

  const [promptText, setPromptText] = useState("");
  const [responseText, setResponseText] = useState("");

  const reset = () => {
    setPromptText("");
    setResponseText("");
  }

  function makeConversation (text) {
    window.alert(text);
  }

    return (
      <div className="mx-auto bg-gray-200 rounded-xl shadow border p-10 flex">
          <ConversationUI promptText={promptText} 
          setPromptText={setPromptText} resetFunction={reset}
          makeConversation={makeConversation}
          responseText={responseText}></ConversationUI>      
          <SupportPanel setPromptText={setPromptText}></SupportPanel>      
      </div>
    );
  }
  
  export default MainPage;
  