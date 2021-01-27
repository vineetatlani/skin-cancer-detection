from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from os import remove
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

model = load_model('skin_cancer_detection-6.h5')

def pred_result(filepath):
    test_image = image.load_img(filepath, target_size = (256,256))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    test_image = test_image/255.0
    result = model.predict(test_image)
    return result[0]


ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
app = Flask(__name__)
app.secret_key = 'this is my secret kry'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('other.html')

@app.route('/process', methods=['POST'])
def process():
    if 'image' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['image']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filepath = 'images/'+secure_filename(file.filename)
        file.save(filepath)
        result = pred_result(filepath)
        if result[0] > result[1]:
            result = "Benign, with probability" + str(result[0])
        else:
            result = "Malignant, with probability" + str(result[1])
        remove(filepath)
        return render_template('other.html', result=result)

    return render_template('other.html')

if __name__ == "__main__":
    app.run(debug=True)
