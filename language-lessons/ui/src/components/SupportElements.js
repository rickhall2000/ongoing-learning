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

function SupportPanel() {
  const [translatedText, setTranslatedText] = useState("Test State");
  const [rawText, setRawText] = useState("Raw text");
  const [guessText, setGuessText] = useState("");
  const [targetLanguage, setTargetLanguage] = useState("fr");
  const [sourceLanguage, setSourceLanguage] = useState("en");
  const [audioFile, setAudioFile] = useState();
  const [recordedAudio, setRecordedAudio] = useState();
  const [transcriptLanguage, setTranscriptLanguage] = useState("en" ); 


  function translateText() {
    fetchTranslation(rawText, (data) => setTranslatedText(data),
      targetLanguage, sourceLanguage);
  }

  const axios = require('axios');

  function transcriptLanguageToLanguageCode(language) {
    console.log(language);
    switch (language) {
      case "en":
        return "en-US";
      case "fr":
        return "fr-FR";
      case "es":
        return "es-ES";
      case "de":
        return "de-DE";
    }
  }

  function invokeGetTranscript() {
    console.log("invokeGetTranscript");
    let langCode = transcriptLanguageToLanguageCode(transcriptLanguage);
    console.log(langCode);
    getTranscript(recordedAudio, langCode,  (data) => setRawText(data))
  }

  function textToSpeech(text, sourceLanguage) {
    getRecording(text, sourceLanguage, (audio) => {
      setAudioFile(audio);
      console.log(audio);
      const player = new Audio(audio);
      player.play();    
    }) 
  }

  function clearState() {
    setTranslatedText("");
    setRawText("");
    setGuessText("");
  }

  return (
    <div className="container bg-gray-50 ml-20 shadow-md w-full">

      <Recorder recordedAudio={recordedAudio} setRecordedAudio={setRecordedAudio}>
      </Recorder>
      <div className='my-3'>
        <Label>Target Language</Label>
        <LanguageDropDown value={targetLanguage} callback={setTargetLanguage}></LanguageDropDown>
        </div>
        <div className='my-3'>
        <Label>Source Language</Label>
        <LanguageDropDown value={sourceLanguage} callback={setSourceLanguage}></LanguageDropDown>
      </div>
      <div>
        <Label>Transcript Language</Label>
        <LanguageDropDown value={transcriptLanguage} callback={setTranscriptLanguage}></LanguageDropDown>
      </div>
      <div className="w-full px-2">
        <Button onClick={invokeGetTranscript}>Show Transcript</Button>
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
      </div>
      <div className="w-full px-2">
        <Button
          onClick={clearState}>Reset</Button>
      </div>
    </div>
  )
}

export default SupportPanel