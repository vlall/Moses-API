from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions
import subprocess
import yaml

app = FlaskAPI(__name__)

def translate(text):
    """
    Run translation model from Docker
    """
    with open('../config.yaml', 'r') as f:
        config = yaml.load(f)
    fileIn = doc["arabic"]["in.file"]
    fileOut = doc["arabic"]["out.file"]
    status = 'Files Read'
    try:
        subprocess.call("rm %s && rm %s" % (fileIn, fileOut))
    except:
        pass
    try:
        translateMe = open(fileIn, w)
        translateMe.write(text)
    translateMe.close()
    except Exception:
        raise('Error creating input file')
    subprocess.call("bin/pipeline-recase.sh < in.file > out.file")
    translatedText = open(fileOut, r)
    fileOut.close()
    return {
            'status': status,
            'url': request.host_url.rstrip('/'),
            'input_text': text,
            'input size': len(text),
            'translation': translatedText,
            'lan': 'N/A',
            'gender': 'N/A'
    }

@app.route("/", methods=['GET'])
def instructions():
    """
    User Instructions
    """
    return 'The Moses API is working! Try a GET request with text.'

@app.route("/<text>", methods=['GET'])
def user_get(text):
    """
    Translate text
    """
    text = translate(text)
    return text
