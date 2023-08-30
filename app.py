from flask import Flask, render_template, request, redirect, Response
import jwt
from transformers import DetrForObjectDetection, DetrImageProcessor 
from PIL import Image
import torch
import time
import datetime
import numpy as np
from camera import VideoCamera
import cv2
import os

app = Flask(__name__)
camera=cv2.VideoCapture(0)


def load_model(saved_model_name):
    processor = DetrImageProcessor.from_pretrained(saved_model_name)
    model = DetrForObjectDetection.from_pretrained(saved_model_name)
    return model, processor

# Model name/path
saved_model_name = 'facebook/detr-resnet-50'    # Replace with trained model name/path 

# Load model only once
model, processor = load_model(saved_model_name)

def predict(frame, min_acc):
      image = Image.fromarray(np.uint8(frame)).convert('RGB')
      inputs = processor(images=image, return_tensors="pt")
      outputs = model(**inputs)
      target_sizes = torch.tensor([image.size[::-1]])
      results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=min_acc)[0]
      print('==========')
      for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
          box = [int(i) for i in box.tolist()]
          msg = f"Detected {model.config.id2label[label.item()]} with confidence {round(score.item(), 3)} at {datetime.datetime.now()}"
          print(msg)
          if os.path.exists('logs.txt') is False:
              with open('logs.txt', 'w') as f:
                  f.write(msg)
          else:
              with open('logs.txt', 'a') as f:
                  f.write('\n' + msg)

          frame = cv2.rectangle(frame, box[:2], box[-2:], [255,255,255], 4)
          frame = cv2.putText(frame, model.config.id2label[label.item()], box[-2:], cv2.FONT_HERSHEY_SIMPLEX,
                   1, (255, 0, 0), 1, cv2.LINE_AA)
      return frame



### Defining Functions
def generate_frames():
    now = datetime.timedelta(datetime.datetime.now().minute)
    while True:
        next1 = datetime.timedelta(datetime.datetime.now().minute)
        ## Read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            # Check frames every 5 minutes
            if next1.days-now.days == 5:
                now = next1
                next1 = datetime.timedelta(datetime.datetime.now().minute)
                # print(next1.days-now.days)
                frame = predict(frame, min_acc=0.8)
                # cv2.imwrite('1.jpg', frame)             # save image
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
'''
def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        #yield (b'--frame\r\n'
        #       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        yield(frame)
'''
        
if __name__ == '__main__':
    app.run(debug=True, port=8000)
