from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

def translate(text):
    """
    TO-DO: Call Moses obj
    """
    return {
        'url': request.host_url.rstrip('/'),
        'text': ('example \'%s\' translation' % (text)),
        'size': len(text),
        'lan': 'Lorem Ipsum',
        'gender': 'Lorem Ipsum'
    }


@app.route("/", methods=['GET'])
def instructions():
    """
    Moses Instructions
    """
    return 'The Moses API is working! Try a GET request with text.'


@app.route("/<text>", methods=['GET'])
def user_get(text):
    """
    Translate text
    """
    text = translate(text)
    return text


if __name__ == "__main__":
    app.run(debug=True)
