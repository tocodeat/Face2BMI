from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input

app = Flask(__name__)

# Global variables to store the webcam and captured image
webcam = None
captured_image = None

# Load the trained model
model = load_model('trained_model (1).h5')

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
      <head>
        <title>BMI Prediction</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
        <script>
          $(document).ready(function() {
            const openWebcamButton = $('#open-webcam');
            const captureImageButton = $('#capture-image');
            const predictButton = $('#predict-bmi');
            const webcamPreview = $('#webcam-preview')[0];
            const capturedImagePreview = $('#captured-image-preview')[0];

            openWebcamButton.on('click', async function() {
              try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                webcamPreview.srcObject = stream;
                webcam = stream;
                captureImageButton.prop('disabled', false);
              } catch (error) {
                console.error('Error accessing webcam:', error);
              }
            });

            captureImageButton.on('click', function() {
              const canvas = document.createElement('canvas');
              const context = canvas.getContext('2d');
              canvas.width = webcamPreview.videoWidth;
              canvas.height = webcamPreview.videoHeight;
              context.drawImage(webcamPreview, 0, 0, canvas.width, canvas.height);
              capturedImagePreview.src = canvas.toDataURL('image/jpeg');
              capturedImagePreview.style.display = 'block';
              capturedImagePreview.style.width = '320px';
              capturedImagePreview.style.height = '240px';
              captured_image = canvas.toDataURL('image/jpeg');
              predictButton.prop('disabled', false);
            });

            predictButton.on('click', async function() {
              try {
                const response = await fetch('/predict', {
                  method: 'POST',
                  body: JSON.stringify({ image: captured_image }),
                  headers: { 'Content-Type': 'application/json' }
                });

                const data = await response.json();
                alert('Predicted BMI: ' + data.bmi.toFixed(2));
              } catch (error) {
                console.error('Error predicting BMI:', error);
              }
            });
          });
        </script>
      </head>
      <body>
        <h1>BMI Prediction</h1>
        <button id="open-webcam">Open Webcam</button>
        <button id="capture-image" disabled>Capture Image</button>
        <button id="predict-bmi" disabled>Predict BMI</button>
        <video id="webcam-preview" width="320" height="240" autoplay></video>
        <img id="captured-image-preview" style="display: none;">
      </body>
    </html>
    '''
@app.route('/predict', methods=['POST'])
def predict():
    image_data = request.json['image']
    image_data = image_data.replace('data:image/jpeg;base64,', '')
    nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image = cv2.resize(image, (160, 160))
    image = img_to_array(image)
    image = image.astype('float32')
    image = preprocess_input(image)
    image = np.expand_dims(image, axis=0)
    
    # Debug statements
    print("Shape of input image:", image.shape)
    print("Pixel values of input image:", image)
    
    prediction = model.predict(image)
    bmi = prediction[0][0]
    
    # Debug statements
    print("Predicted BMI:", bmi)
    
    return jsonify({'bmi': float(bmi)})

if __name__ == '__main__':
    app.run(debug=True, port=5004)
