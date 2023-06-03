# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
from face_detect import detect_faces
from gun_detect import detect_weapon

# creating a Flask app
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if (request.method == 'GET'):
        token = detect_weapon()
        token1 = detect_faces()
        severity = 0
        severity = token + token1
        count=0
        while(count!=3):
            pin=345467
            count+=1
            if(pin=="12345"):
                if(count>1):
                    severity+=0
            else:
                print("Wrong PIN")
                severity+=3
        if(count==3):
            severity+=10
    return jsonify({'Level': severity})




# driver function
if __name__ == '__main__':

	app.run(debug = True, port=8000)
