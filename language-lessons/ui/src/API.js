import axios from 'axios';
import configData from './config.json';
const apiURLBase = configData.SERVER_URL;
const apiKey = configData.API_KEY;

let defaultOptions = {"headers": {"x-api-key": apiKey}} ;

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

export function getTranscript(file, language, action) {
  let url = apiURLBase + "transcribe";

  const reader = new FileReader();

  reader.addEventListener("loadend", () => {

    const request_data = {"file": reader.result, language}
    axios.post(url, request_data, defaultOptions).then(function (response) {
        let { data } = response;
        action(data);
      }
  )
    
});

  reader.readAsDataURL(file);
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
