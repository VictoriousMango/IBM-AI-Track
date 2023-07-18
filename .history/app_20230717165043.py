from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def hello_world():
    return render_template('email.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)