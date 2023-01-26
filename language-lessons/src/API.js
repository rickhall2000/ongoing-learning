import axios from 'axios';
import configData from './config.json';
const apiURLBase = configData.SERVER_URL;
const apiKey = configData.API_KEY;

let defaultOptions = {"headers": {"x-api-key": apiKey}} ;

// todo: find the right params for the api, dummy

export function fetchTranslation(source_text, action, target_language="fr", source_language="en") {
    let url = apiURLBase + "translate";

    let data = {"text": source_text,
                "from": source_language,
                "to": target_language,};

    axios.post(url=url, 
              data=data, 
              defaultOptions).then(function (response) {
        let { data } = response;
      action(data);
    })  
};

export function getTranscript(audio, language, action) {
  let url = apiURLBase + "transcribe";
  /*let data = new FormData();

  data.append('wavfile', audio, 'example.wav');    
  data.append("language", language);
 */

  let data = {"text": "This is just a dummy"};

      const config = {
//        headers: { 'content-type': 'multipart/form-data', }
      };

      axios.post(url, data, config).then(function (response) {
          let { data } = response;
          action(data);
        }
      )
}

export function getRecording(text, language, action) {
  let url = apiURLBase + "speak"

  let data = {"text": text,
              "language": language}
  
  axios.post(url=url, data=data, defaultOptions).then(function (response) {
    let { data } = response;
    action(data);
  })
}
