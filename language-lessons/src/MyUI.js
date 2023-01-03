import React, { useState } from 'react';

// todo: add tailwind css to give it some style
// todo: add http library for API calls
// todo: Do someting with the text boxes 
// todo: -- step one, make the show translation button copy text from source to translation
// todo: -- should put ids on these components, right?
// todo: reset should clear all the things

function GenericButtonClick() {
  window.alert("You clicked me");
}

function Button() {
  return <button onClick={GenericButtonClick}>Record phrase</button>
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
    <>
      <div>
        <Button>Record Audio</Button>
      </div>
      <div>
        <button onClick={() => window.alert("Transcript button click")}>Show Transcript</button>
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
        <button onClick={doTranslation}>Show Translation</button>
      </div>
      <div>
        <label>Translation</label>
        <textarea type="text" readOnly={true}  value={translatedText}></textarea>
      </div>
      <div>
        <button onClick={clearState}>Reset</button>
      </div>
    </>
  )
}

export default MyThing