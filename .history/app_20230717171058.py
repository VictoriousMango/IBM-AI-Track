from flask import Flask, render_template, request, redirect

app = Flask(__name__)
  

@app.route("/", methods=['POST', 'GET'])
def hello_world():
    email, password = 0, 0
    if request.method == 'POST':
        values = []
        for i in request.form:
            values.append(i)
        email, password = values[0], values[1]
        return redirect(f'/Home-Page/{email}/{password}')
    return render_template('email.html')

@app.route('/Home-Page/<string:email>/<string:password>')
def HomePage(email, password):
    return render_template('HomePage.html', email=email, password=password)

if __name__ == '__main__':
    app.run(debug=True, port=8000)