from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

def translate(text):
    return {
        'url': request.host_url.rstrip('/'),
        'text': ('example \'%s\' translation' % (text))
        'wc':(len(text))
        'lan': 'Lorem Ipsum'
        'gender': 'Lorem Ipsum'
    }


@app.route("/", methods=['GET'])
def notes_list():
    """
    List or create notes.
    """
    return 'The Moses API is working! Try a GET request with text.'


@app.route("/<text>", methods=['GET'])
def notes_detail(text):
    """
    Retrieve, update or delete note instances.
    """
    text = translate(text)
    return text


if __name__ == "__main__":
    app.run(debug=True)
