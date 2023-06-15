# Face2BMI
This repository hosts a Flask-based web API project that uses a deep learning model built on the InceptionResNetV2 architecture for real-time Body Mass Index (BMI) estimation from webcam images. It provides users the ability to capture images through their webcam and receive immediate BMI predictions, thereby creating an interactive and intuitive experience for BMI estimation

## Project Structure
* app.py: The main application file where the Flask app and routes are defined.
* model.html : An HTML file that contains code which, when run, generates the trained deep learning model and saves it in the 'model/' directory.
* requirements.txt: File listing the Python dependencies required for this project.

## Installation & Usage
1. Clone the repository.
3. Navigate to the project directory and create a virtual environment (python -m venv myenv).
4. Activate the virtual environment (source myenv/bin/activate for Linux/Mac and myenv\Scripts\activate for Windows).
5. Install the required dependencies (pip install -r requirements.txt).
6. Run the code in model.html to generate the trained model.
7. Run the Flask application (python app.py).
8. Open your web browser and enter the URL where the web API is running (e.g., http://localhost:5004).
9. Follow the instructions on the web page to capture an image and get the BMI prediction.

Please note that the trained model is not included in this repository due to size constraints. After running the code in model.html, the generated model should be placed in the model directory and will be used by app.py for BMI prediction.

## Results
The trained model achieved a mean absolute error of 6.2451 on the test set, demonstrating its ability to make reasonably accurate and reliable predictions of BMI from image data.

## Future Improvements
* Incorporation of additional data sources or features to enhance prediction accuracy.
* Model fine-tuning with a larger and more diverse dataset.
* User feedback integration to continuously improve the model over time.
