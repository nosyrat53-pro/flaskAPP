from flask import Flask, request, jsonify, render_template, url_for, send_file
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from rembg import remove
import easygui
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'  # Specify the folder where uploaded images will be stored
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define the route for image upload


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Secure the filename to prevent any malicious input
    filename = secure_filename(image_file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Save the uploaded image
    image_file.save(filepath)

    # Remove background using OpenCV
    final_image = remove_background(filepath)

    output_filename = 'IMAGENice.jpg'

    output_filepath = os.path.join(
        app.config['UPLOAD_FOLDER'], output_filename)

    # save proccessed image
    cv2.imwrite(output_filepath, final_image)
    return send_file(output_filepath)

    # return jsonify({'message': 'Image uploaded and processed successfully', 'filename': output_filename})


def remove_background(image_path):
    # input = Image.open(image_path)
    input = cv2.imread(image_path)
    output = remove(input)

    return output


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
