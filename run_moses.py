from api.moses_api import app

def main():
    app.run(
            host='0.0.0.0',
            port=5000,
            threaded=True,
            debugging=True
    )


if __name__ == '__main__':
    main()