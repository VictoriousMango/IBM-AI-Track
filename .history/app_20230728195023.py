from flask import Flask, render_template, request, redirect, Response
import jwt
from camera import VideoCamera
import cv2

app = Flask(__name__)
camera=cv2.VideoCapture(0)

### Defining Functions
def generate_frames():
    while True:
        ## Read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        
        yield(b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


### Defining Routes

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

@app.route('/Home-Page/')
def Email():
    return redirect('/')


@app.route('/Home-Page/<string:message_jwt>')
def HomePage(message_jwt):
    decoded_jwt = jwt.decode(message_jwt, "secret", algorithms=["HS256"])
    
    return render_template('HomePage.html', j_w_t=message_jwt, email=decoded_jwt['email'], password=decoded_jwt['password'], user=decoded_jwt['email'].split('@')[0])


@app.route('/Login1')
def Login1():
    return render_template('/Login1.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    #return render_template('/video.html')
def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        #yield (b'--frame\r\n'
        #       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        yield(frame)

if __name__ == '__main__':
    app.run(debug=True, port=8000)