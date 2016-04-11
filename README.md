[![Build Status](https://travis-ci.org/vlall/Moses-API.svg?branch=master)](https://travis-ci.org/vlall/Moses-API)
# Moses-API
Build a RESTful API server running your own machine translation model

### Instructions
- First pull the Docker image 

  ```$ docker pull vlall/moses-api```

- Next, run the image and forward from 5000 to the local port you want the API to be running on
    ```
    $ docker run -pit 5000:5000 vlall/moses-api
    ```

- You will be directed to the /mosesdecoder directory. Here is where you will compile Moses (takes a few minutes to run).
    ```
    $ ./bjam --with-boost=/home/moses/Downloads/boost_1_60_0 --with-cmph=/home/moses/cmph-2.0 --with-irstlm=/home/moses/irstlm -j12
    ```

- Your Docker image is already modified to work with the sample model. Use /home/moses/Downloads/moses-api/config.yaml as a reference for integration with your own models.

- Start your RESTful API server in the background

    ```$ python run_moses.py &```

- For a quick translation, run:

    ```
    $ curl -XGET localhost:5000/haus | python -m json.tool
    {
        "CMD": "/home/moses/mosesdecoder/bin/moses -f phrase-model/moses.ini < phrase-model/in > out",
        "DURATION": "0.603 seconds",
        "INPUT": "haus",
        "INPUT_PATH": "/home/moses/moses-models/sample-models/phrase-model/in",
        "INPUT_SIZE": 4,
        "LAN": "N/A",
        "MODEL": "/home/moses/moses-models/sample-models",
        "OUTPUT": "house",
        "OUTPUT_PATH": "/home/moses/moses-models/sample-models/out",
        "OUTPUT_SIZE": 7,
        "STATUS": "Files successfully read",
        "URL": "http://localhost:5000"
    }

    ```

- To translate a whole file, navigate to your /moses-api folder, then run:

    ```
    $ curl -XPUT -F name=@translate_me.txt localhost:5000/upload | python -m json.tool
    {
        "CMD": "/home/moses/mosesdecoder/bin/moses -f phrase-model/moses.ini < phrase-model/in > out",
        "DURATION": "0.624 seconds",
        "INPUT": "das ist ein klein haus\n",
        "INPUT_PATH": "/home/moses/moses-models/sample-models/phrase-model/in",
        "INPUT_SIZE": 23,
        "LAN": "N/A",
        "MODEL": "/home/moses/moses-models/sample-models",
        "OUTPUT": "this is a small house",
        "OUTPUT_PATH": "/home/moses/moses-models/sample-models/out",
        "OUTPUT_SIZE": 24,
        "STATUS": "Files successfully read",
        "URL": "http://localhost:5000"
    }
    ```

Since this the Moses sample-model, it is very limited. Visit the Moses SMT website for more information on creating your own models: http://www.statmt.org/moses/?n=Development.GetStarted
