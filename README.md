[![Build Status](https://travis-ci.org/vlall/Moses-API.svg?branch=master)](https://travis-ci.org/vlall/Moses-API)
# Moses-API
Build an API server running your own machine translation model

### Instructions
- First pull the Docker image 

  ```$ docker pull vlall/moses-api```
  
- See sample-config.yml as a reference.

    ```
    infile: '/home/moses/moses-models/sample-models/phrase-model/in'
    outfile: '/home/moses/moses-models/sample-models/out'
    homeDir: '/home/moses/moses-models/sample-models'
    command: '/home/moses/mosesdecoder/bin/moses -f phrase-model/moses.ini < phrase-model/in > out'
    ```
- Start your API server in the background

    ```$ python run_moses.py &```

- Finally, make a GET request

    ```
    $ curl -XGET localhost:5000/haus | python -m json.tool
    {
        "gender": "N/A",
        "input size": 4,
        "input_text": "haus",
        "lan": "N/A",
        "status": "Files successfully read",
        "translation": "house",
        "url": "http://localhost:5000"
    }


