# Moses-API
Build an API server running your own machine translation model

### Instructions
- First pull the Docker image 

  ```$ docker pull vlall/moses-api```
  
- Edit the config.yaml file to point to your model.

    ```
    infile: "path/to/run/in.file"
    outfile: "path/to/run/out.file"
    ```
- Then do 

    ```$ python run_moses.py```
