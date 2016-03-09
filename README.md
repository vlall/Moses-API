[![Build Status](https://travis-ci.org/vlall/Moses-API.svg?branch=master)](https://travis-ci.org/vlall/Moses-API)
# Moses-API
Build a RESTful API server running your own machine translation model

### Instructions
- First pull the Docker image 

  ```$ docker pull vlall/moses-api```

- Next, run the image and compile Moses in the mosesdecoder directory
    ```
    $ cd /home/moses/mosesdecoder
    $ ./bjam --with-boost=/home/moses/Downloads/boost_1_60_0 --with-cmph=/home/moses/cmph-2.0 --with-irstlm=/home/moses/irstlm -j12
    ```

- Your Docker image is already modified to work with the sample model. Use /home/moses/Downloads/moses-api/config.yaml as a reference for integrating with your own models. 

    ```
    in: '/home/moses/moses-models/sample-models/phrase-model/in'
    out: '/home/moses/moses-models/sample-models/out'
    homeDir: '/home/moses/moses-models/sample-models'
    command: '/home/moses/mosesdecoder/bin/moses -f phrase-model/moses.ini < phrase-model/in > out'
    ```
- Start your RESTful API server in the background

    ```$ python run_moses.py &```

- For a quick translatation of a word, try:

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
    ```

- To translate a whole file, run

    ```
    $ curl -XPUT -F name=@translate_me.txt localhost:5000/upload | python -m json.tool
    {
        "gender": "N/A",
        "input size": 22,
        "input_text": "das ist ein klein haus",
        "lan": "N/A",
        "status": "Files successfully read",
        "translation": "this is a small house",
        "url": "http://localhost:5000"
    }
    ```
