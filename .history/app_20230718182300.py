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
        encoded_jwt = jwt.encode({'email': email, 'password': password}, "secret", algorithm="HS256")
        return redirect(f'/Home-Page/{encoded_jwt}')
    return render_template('email.html')

@app.route('/Home-Page/<string:message_jwt>')
def HomePage(message_jwt):
    decoded_jwt = jwt.decode(message_jwt, "secret", algorithms=["HS256"])
    content = {
        'Username': email.split('@')[0],
        'email': email,
        'password': password
    }
    
    return render_template('HomePage.html', email=decoded_jwt, password=password, user=content['Username'], content=content)

@app.route('/Login1')
def Login1():
    return render_template('/Login1.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)