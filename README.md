[![Build Status](https://travis-ci.org/vlall/Moses-API.svg?branch=master)](https://travis-ci.org/vlall/Moses-API)
# Moses-API
Build an API server running your own machine translation model

### Instructions
- First pull the Docker image 

  ```$ docker pull vlall/moses-api```

- Next, compile moses in the mosesdecoder directory
    ```
    $ /home/moses/mosesdecoder
    $ ./bjam --with-boost=/home/moses/Downloads/boost_1_60_0 --with-cmph=/home/moses/cmph-2.0 --with-irstlm=/home/moses/irstlm -j12
    ```

- See sample-config.yml as a reference for configuring the path to your models.

    ```
    infile: '/home/moses/moses-models/sample-models/phrase-model/in'
    outfile: '/home/moses/moses-models/sample-models/out'
    homeDir: '/home/moses/moses-models/sample-models'
    command: '/home/moses/mosesdecoder/bin/moses -f phrase-model/moses.ini < phrase-model/in > out'
    ```
- Start your API server in the background

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
    $ curl -X PUT -F name=@translate_me.txt localhost:5000/upload | python -m json.tool
    ```


