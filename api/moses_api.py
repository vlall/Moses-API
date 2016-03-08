from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions
import subprocess
import yaml

app = FlaskAPI(__name__)

def translate(text):
    """
    Run translation model from Docker
    """
    with open('sample-config.yaml', 'r') as f:
        doc = yaml.load(f)
    fileIn = doc['sample-models']['infile']
    fileOut = doc['sample-models']['outfile']
    homeDir = doc['sample-models']['homeDir']
    runCommand = doc['sample-models']['command']
    status = 'Files successfully read'
    try:
        subprocess.call(['rm %s && rm %s'] % (fileIn, fileOut))
    except:
        pass
    try:
        translateMe = open(fileIn, w)
        translateMe.write(text)
        translateMe.close()
    except Exception:
        print('Error creating input file')
    subprocess.call([runCommand], cwd=homeDir,shell=True)
    readTranslate = open(fileOut, 'r')
    translatedText = readTranslate.read()
    readTranslate.close()
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
