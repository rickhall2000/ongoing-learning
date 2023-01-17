import axios from 'axios';

const apiURLBase = "https://j27h8nllk4.execute-api.us-east-1.amazonaws.com/dev/";

// todo: find the right params for the api, dummy

export function fetchTranslation(source_text, action, target_language="fr", source_language="en") {
    let url = apiURLBase + "text";

    let data = {"text": source_text,
                "from": source_language,
                "to": target_language,};

    axios.post(url=url, data=data).then(function (response) {
        let { data } = response;
      action(data);
    })  
};

