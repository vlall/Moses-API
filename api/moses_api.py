from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions
import subprocess
import yaml
from werkzeug import secure_filename
import codecs
import json
import time

app = FlaskAPI(__name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def translate(text):
    start_time = time.time()
    """
    Run translation model using config
    """
    with open('/home/moses/Downloads/moses-api/config.yaml', 'r') as f:
        doc = yaml.load(f)
    fileIn = doc['sample-models']['in']
    fileOut = doc['sample-models']['out']
    homeDir = doc['sample-models']['homeDir']
    runCommand = doc['sample-models']['command']
    status = 'Files successfully read'
    subprocess.call(['rm %s && rm %s' % (fileIn, fileOut)], shell=True)
    text8 = text.encode('utf8')
    inputFile = open(fileIn, 'w')
    inputFile.write(text8 + '\n')
    inputFile.close()
    subprocess.call([runCommand], cwd=homeDir, shell=True)
    readTranslate = open(fileOut, 'r')
    translatedText = readTranslate.read().decode('utf8')
    readTranslate.close()
    return {
            "STATUS": status,
            "LAN": 'N/A',
            "MODEL": str(homeDir),
            "CMD": str(runCommand),
            "URL": request.host_url.rstrip('/').decode().encode('utf8'),
            "INPUT": text.encode('utf8'),
            "INPUT_SIZE": len(text.encode('utf8')),
            "INPUT_PATH": str(fileIn),            
            "OUTPUT": translatedText.encode('utf8').rstrip(),
            "OUTPUT_SIZE": len(translatedText.encode('utf8')),
            "OUTPUT_PATH": str(fileOut),
            "DURATION": '%.3f seconds' % (time.time() - start_time)
    }


@app.route("/", methods=['GET'])
def instructions():
    return 'The Moses API is working! Try a GET request with text.\n'


@app.route("/<text>", methods=['GET'])
def user_get(text):
    """
    Translate text
    """
    text = translate(text.decode('utf8'))
    return text


@app.route("/upload", methods=['POST', 'PUT'])
def upload():
    """
    Tranlsate file
    """
    file = request.files['name']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        text = file.read().decode('utf8')
        text = translate(text)
        return text
    else:
        return ('Error reading file...\n')
