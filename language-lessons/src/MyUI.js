import React, { Children, useState } from 'react';
import { fetchTranslation, getTranscript } from "./API";
import Button from "./components/Button"
import LanguageDropDown from './components/LanguageDropDown';
import Recorder from "./components/Recorder"


// todo: make the form better looking
// todo: send audio to API and receive text back
// todo: make working Textarea component
// todo: add permission check to record audio
// todo: send text to API and receive audio back


function MyThing() {
  const [translatedText, setTranslatedText] = useState("Test State");
  const [rawText, setRawText] = useState("Raw text");
  const [guessText, setGuessText] = useState("");
  const [targetLanguage, setTargetLanguage] = useState("fr");
  const [sourceLanguage, setSourceLanguage] = useState("en");


  function translateText() {
    // I want this function to read the text from the "source text" box
    // and write it to the translation text box
    fetchTranslation(rawText, (data) => setTranslatedText(data),
      targetLanguage, sourceLanguage);
  }

  function speechToText() {
    getTranscript("audio goes here", sourceLanguage, console.log);
  }

  function clearState() {
    setTranslatedText("");
    setRawText("");
    setGuessText("");
  }


  return (
    <div className="container bg-gray-50 ml-20 shadow-md w-1/4">

      <Recorder>
      </Recorder>

      <div>
        <label>Target Language</label>
        <LanguageDropDown value={targetLanguage} callback={setTargetLanguage}></LanguageDropDown>
        <label>Source Language</label>
        <LanguageDropDown value={sourceLanguage} callback={setSourceLanguage}></LanguageDropDown>
      </div>
      <div className="w-full px-2">
        <Button onClick={speechToText}>Show Transcript</Button>
      </div>
      <div className="w-full px-2">
        <label className="font-bold block text-lg">Source Text</label>
        <textarea
          className="p-1 text-lg ring ring-gray-400 focus:bg-yellow-50 
          focus:outline-none rounded w-full h-24"
          value={rawText}
          onChange={(event) => setRawText(event.target.value)}
        ></textarea>
      </div>
      <div className="w-full px-2">
        <label className="font-bold block text-lg">My Translation</label>
        <textarea
          className="p-1 text-lg ring ring-gray-400 focus:bg-yellow-50 
      focus:outline-none rounded w-full h-24"
          value={guessText}
          onChange={(event) => setGuessText(event.target.value)}
        ></textarea>
      </div>
      <div className="w-full px-2">
        <Button onClick={translateText}
        >Show Translation</Button>
      </div>
      <div className="w-full px-2">
        <label className="font-bold block text-lg">Translation</label>
        <textarea type="text" readOnly={true}
          className="p-1 text-lg ring ring-gray-400 focus:bg-yellow-50 
          focus:outline-none rounded w-full h-24"
          value={translatedText}></textarea>
      </div>
      <div className="w-full px-2">
        <Button
          onClick={clearState}>Reset</Button>
      </div>
    </div>
  )
}

export default MyThing