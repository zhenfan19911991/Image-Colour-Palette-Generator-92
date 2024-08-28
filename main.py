from flask import Flask, abort, render_template, redirect, url_for, flash, request
from werkzeug.utils import secure_filename
import os
import numpy as np
from PIL import Image # for reading image files


UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def frequency(arr):
    reshape_d = arr.shape[0]* arr.shape[1]
    y= arr.reshape(reshape_d,3)

    unique, counts = np.unique(y, return_counts=True, axis = 0)
    xl = [tuple(row) for row in unique]
    re = {}
    for n in range(0,len(xl)):
        xl[n] = '#%02x%02x%02x' % tuple(int(x) for x in xl[n])
        re[xl[n]] = round(int(counts[n])/reshape_d,4)

    re = sorted(re.items(), key=lambda x: x[1], reverse=True)
    re = [[n[0], format(n[1], ".2%")] for n in re]
    return re



@app.route('/', methods=['GET', 'POST'])
def home():
    file_path = ''
    freq_top10 = None

    if request.method == 'POST':
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')

        elif not allowed_file(file.filename):
            flash('Only .png, .jpg and .jpeg files are acceptable')
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'uploaded_image.{filename.rsplit('.', 1)[1].lower()}')
            file.save(file_path)

            my_img = Image.open(file_path).convert('RGB')
            img_array = np.array(my_img)
            freq_top10 = frequency(img_array)[:10]

    return render_template('index.html', image = f'{file_path}', top_color = freq_top10)
















if __name__ == "__main__":
    app.run(debug=True)