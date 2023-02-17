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

//const axios = require('axios');

async function uploadFileToTranscribe(file, language) {
  const url = '<your_api_gateway_url>'; // Replace with your API Gateway endpoint URL
  const headers = { 'Content-Type': 'application/json' };
  const data = { file, language };

  try {
    const response = await axios.post(url=url, data=data, defaultOptions);
    console.log(response);
  } catch (error) {
    console.error(error);
  }
}

export function getTranscript(file, language, action) {
  let url = apiURLBase + "transcribe";
  console.log(file);
  let data = new FormData();


const reader = new FileReader();

reader.addEventListener("loadend", () => {
  // reader.result contains the contents of blob as a typed array
  console.log(reader.result);

  const request_data = {"file": reader.result, language}
  const config = {
            headers: { 'content-type': 'application.json'}
          };
    
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
