import React, { Children, useState } from 'react';
import axios from 'axios';
import MicRecorder from 'mic-recorder-to-mp3'

// todo: make the form better looking
// todo: move Button into its own file
// todo: send audio to API and receive text back
// todo: make working Textarea component
// todo: add permission check to record audio

/*
sample of checking permission to use audio
need to do this functionally. There is probably a hook for that

  componentDidMount() {
    navigator.getUserMedia({ audio: true },
      () => {
        console.log('Permission Granted');
        this.setState({ isBlocked: false });
      },
      () => {
        console.log('Permission Denied');
        this.setState({ isBlocked: true })
      },
    );
  }

*/


const Mp3Recorder = new MicRecorder({ bitRate: 128 });

function doIHaveAxios(){
  axios.get("https://www.google.com")
  return "Cool"
}

function Button({children, onClick, disabled=false}) {
  return <button className="bg-blue-500 text-white"
  disabled={disabled}  
  onClick={onClick}>{children}</button>
}



function MyThing() {
  const [translatedText, setTranslatedText] = useState("Test State");
  const [rawText, setRawText] = useState("Raw text");
  const [guessText, setGuessText] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [blobURL, setBlobURL] = useState('');
  const [isBlocked, setIsBlocked] = useState(false);

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

  function doTranslation() {
    setTranslatedText(rawText);
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
        <Button 
          onClick={() => startRecordingClick()}
          disabled={isRecording}
        >Start Recording</Button>
      </div>
      <div>
        <Button
          onClick={() => stopRecordingClick()}
          disabled={!isRecording}
        >Stop Recording</Button>
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