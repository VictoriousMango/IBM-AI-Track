from flask import Flask, render_template, request, redirect
import jwt

app = Flask(__name__)
  

@app.route("/", methods=['POST', 'GET'])
def hello_world():
    email, password = 0, 0
    if request.method == 'POST':
        values = []
        for i in request.form:
            values.append(request.form[i])
        email, password = values[0], values[1]
        encoded_jwt = jwt.encode(email+password, "secret", algorithm="HS256")
        return redirect(f'/Home-Page/{email}/{password}')
    return render_template('email.html')

@app.route('/Home-Page/<string:email>/<string:password>')
def HomePage(email, password):
    content = {
        'Username': email.split('@')[0],
        'email': email,
        'password': password
    }
    return render_template('HomePage.html', email=email, password=password, user=content['Username'], content=content)

if __name__ == '__main__':
    app.run(debug=True, port=8000)