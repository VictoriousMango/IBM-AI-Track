from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def hello_world():
    email, password = 0, 0
    if request.method == 'POST':
        email, password = request.form
        return redirect('HomePage.html', email=email, password=password)
    return render_template('email.html')

@app.route('/Home-Page')
def HomePage():
    return render_template('HomePage.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)