import React, { Children, useState } from 'react';
import { fetchTranslation, getTranscript, getRecording } from "../API";
import Button from "./Button"
import Label from "./Label"
import LanguageDropDown from './LanguageDropDown';
import Recorder from "./Recorder"


// todo: make the form better looking
// todo: send audio to API and receive text back
// todo: make working Textarea component
// todo: add permission check to record audio
// todo: make this page contain the old ui and chat gpt components

function SupportPanel({setPromptText}) {
  const [translatedText, setTranslatedText] = useState("Test State");
  const [rawText, setRawText] = useState("Raw text");
  const [guessText, setGuessText] = useState("");
  const [targetLanguage, setTargetLanguage] = useState("fr");
  const [sourceLanguage, setSourceLanguage] = useState("en");
  const [audioFile, setAudioFile] = useState();
  const [recordedAudio, setRecordedAudio] = useState();


  function translateText() {
    fetchTranslation(rawText, (data) => setTranslatedText(data),
      targetLanguage, sourceLanguage);
  }

  const axios = require('axios');

  function invokeGetTranscript() {
    getTranscript(recordedAudio, sourceLanguage, console.log)
  }

  function textToSpeech(text, sourceLanguage) {
    getRecording(text, "en-US", (audio) => {
      setAudioFile(audio);
      console.log(audio);
      const player = new Audio(audio);
      player.play();    
    }) 
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

      <Recorder recordedAudio={recordedAudio} setRecordedAudio={setRecordedAudio}>
      </Recorder>
      <div>
        <Button onClick={invokeGetTranscript}>Invoke Transcribe</Button>
      </div>
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
        <Label>Source Text</Label>
        <textarea
          className="p-1 text-lg ring ring-gray-400 focus:bg-yellow-50 
          focus:outline-none rounded w-full h-24"
          value={rawText}
          onChange={(event) => setRawText(event.target.value)}
        ></textarea>
        <Button onClick={() => textToSpeech(rawText, sourceLanguage)}>Hear This</Button>
        <Button onClick={() => setPromptText(rawText)}>Send to GPT propt</Button>
      </div>
      <div className="w-full px-2">
        <Label>My Translation</Label>
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
        <Label>Translation</Label>
        <textarea type="text" readOnly={true}
          className="p-1 text-lg ring ring-gray-400 focus:bg-yellow-50 
          focus:outline-none rounded w-full h-24"
          value={translatedText}></textarea>
        <Button onClick={() => setPromptText(translatedText)}>Send to GPT propt</Button>
      </div>
      <div className="w-full px-2">
        <Button
          onClick={clearState}>Reset</Button>
      </div>
    </div>
  )
}

export default SupportPanel