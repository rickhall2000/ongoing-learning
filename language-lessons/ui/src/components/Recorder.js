import React, { Children, useState } from 'react';
import Button from './Button'
import MicRecorder from 'mic-recorder-to-mp3'


const Mp3Recorder = new MicRecorder({ bitRate: 128 });


function Recorder() {

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
          console.log(blob);
          const blobURL = URL.createObjectURL(blob);
          setBlobURL(blobURL);
          setIsRecording(false);
          console.log(typeof(blob));
          const player = new Audio(URL.createObjectURL(blob));
          player.play();    
        }).catch((e) => console.log(e));
    };
    
    
    function startRecordingClick() {
      console.log("Start clicked");
      start();
          setIsRecording(true);
    }
    
    function stopRecordingClick() {
      console.log("stop clicked");
      stop();
          setIsRecording(false);
    }
    

    return <div>
        <div className="w-full px-2">
            <Button
                      onClick={() => startRecordingClick()}
                      disabled={isRecording}
            >Start Recording </Button>
        </div>
        <div className="w-full px-2">
            <Button
                      onClick={() => stopRecordingClick()}
                      disabled={!isRecording}
            >Stop Recording</Button>
        </div>

    </div>

}

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


export default Recorder;