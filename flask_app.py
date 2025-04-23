from flask import Flask

app = Flask(__name__, static_url_path='', static_folder='staticpages')

@app.route('/')
def index():
    return "test"

if __name__ == "__main__":
    app.run(debug=True)