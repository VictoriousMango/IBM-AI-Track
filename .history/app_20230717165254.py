from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        return render_template('HomePage.html')
    return render_template('email.html')

@app.route('/Home-Page')
def HomePage():
    return render_template('HomePage.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)