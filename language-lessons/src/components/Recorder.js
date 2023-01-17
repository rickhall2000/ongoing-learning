import Button from './Button'


function Recorder() {
    return <div>
        <div className="w-full px-2">
            <Button
            //          onClick={() => startRecordingClick()}
            //          disabled={isRecording}
            >Start Recording </Button>
        </div>
        <div className="w-full px-2">
            <Button
            //          onClick={() => stopRecordingClick()}
            //          disabled={!isRecording}
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