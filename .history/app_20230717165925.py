from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def hello_world():
    email, password = 0, 0
    if request.method == 'POST':
        #email, password = request.form
        return redirect('HomePage.html')
    return render_template('email.html')

@app.route('/HomePage')
def HomePage():
    return render_template('HomePage.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)