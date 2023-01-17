import React, { Children, useState } from 'react';
import MicRecorder from 'mic-recorder-to-mp3'
import { fetchTranslation } from "./API";
import Button from "./components/Button"
import Recorder from "./components/Recorder"


// todo: make the form better looking
// todo: send audio to API and receive text back
// todo: make working Textarea component
// todo: add permission check to record audio
// todo: move recorder controls to separate file




const Mp3Recorder = new MicRecorder({ bitRate: 128 });


function MyThing() {
  const [translatedText, setTranslatedText] = useState("Test State");
  const [rawText, setRawText] = useState("Raw text");
  const [guessText, setGuessText] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [blobURL, setBlobURL] = useState('');
  const [isBlocked, setIsBlocked] = useState(false);


  function translateText() {
    // I want this function to read the text from the "source text" box
    // and write it to the translation text box
    fetchTranslation(rawText, (data) => setTranslatedText(data),
      "fr", "en");
  }

  let start = () => {
    if (isBlocked) {
      console.log('Permission Denied');
    } else {
      Mp3Recorder
        .start()
        .then(() => {
          setIsRecording(true);
        }).catch((e) => console.error(e));
    }
  };

  let stop = () => {
    Mp3Recorder
      .stop()
      .getMp3()
      .then(([buffer, blob]) => {
        const blobURL = URL.createObjectURL(blob);
        setBlobURL(blobURL);
        setIsRecording(false);

        const player = new Audio(URL.createObjectURL(blob));
        player.play();

      }).catch((e) => console.log(e));
  };


  function clearState() {
    setTranslatedText("");
    setRawText("");
    setGuessText("");
  }

  function startRecordingClick() {
    console.log("Start clicked");
    start();
    //    setIsRecording(true);
  }

  function stopRecordingClick() {
    console.log("stop clicked");
    stop();
    //    setIsRecording(false);
  }
  return (
    <div className="container bg-gray-50 ml-20 shadow-md w-1/4">

      <div>
      </div>
      <div className="w-full px-2">
        <Button
          onClick={() => startRecordingClick()}
          disabled={isRecording}
        >Start Recording</Button>
      </div>
      <div className="w-full px-2">
        <Button
          onClick={() => stopRecordingClick()}
          disabled={!isRecording}
        >Stop Recording</Button>
      </div>
      <div className="w-full px-2">
        <Button onClick={() => translateText()}>Show Transcript</Button>
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