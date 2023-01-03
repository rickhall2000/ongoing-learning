import React, { Children, useState } from 'react';
import axios from 'axios';

// todo: make the form better looking
// todo: move Button into its own file
// todo: add http library for API calls
// todo: figure out how to record from microphone
// todo: make working Textarea component


function doIHaveAxios(){
  axios.get("www.google.com")
  return "Cool"
}

function Button({children, onClick}) {
  return <button className="bg-blue-500 text-white"  
  onClick={onClick}>{children}</button>
}

function Textarea({value, onChange}) {
  return <textarea className="bg-blue-50"></textarea>
  value={value}
  onChange={onChange}
}

function MyThing() {
  const [translatedText, setTranslatedText] = useState("Test State");
  const [rawText, setRawText] = useState("Raw text")
  const [guessText, setGuessText] = useState("")
  
  function clearState() {
    setTranslatedText("");
    setRawText("");
    setGuessText("");
  }

  function doTranslation() {
    setTranslatedText(rawText);
  }

  return (
    <div className="container bg-gray-50 ml-20 shadow-md w-1/4">
      <div>
        <Button 
        onClick={() => window.alert("Record button click")}
        >Record Audio</Button>
      </div>
      <div>
        <Button onClick={() => doIHaveAxios()}>Show Transcript</Button>
      </div>
      <div>
        <label>Source Text</label>
        <textarea  
          value={rawText}
          onChange={(event) => setRawText(event.target.value)}
        ></textarea>
      </div>
      <div>   
        <label>My Translation</label>
        <textarea 
          type="text"
          value={guessText}
          onChange={(event) => setGuessText(event.target.value)}
        ></textarea>
      </div>
      <div>
        <Button onClick={doTranslation}>Show Translation</Button>
      </div>
      <div>
        <label>Translation</label>
        <textarea type="text" readOnly={true}  value={translatedText}></textarea>
      </div>
      <div>
        <Button
        onClick={clearState}>Reset</Button>
      </div>
    </div>
  )
}

export default MyThing