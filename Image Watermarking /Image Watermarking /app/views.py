# Important imports
from app import app
from flask import request, render_template
import os
import cv2
import numpy as np
from PIL import Image
from datetime import datetime  # Importing datetime module

# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():
    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # Execute if request is get
    if request.method == "GET":
        return render_template("index.html", timestamp=timestamp)

    # Execute if request is post
    if request.method == "POST":
        option = request.form['options']
        image_upload = request.files['image_upload']
        imagename = image_upload.filename
        image = Image.open(image_upload)
        image_logow = np.array(image.convert('RGB'))
        h_image, w_image, _ = image_logow.shape
        
        if option == 'logo_watermark':
            logo_upload = request.files['logo_upload']
            logoname = logo_upload.filename
            logo = Image.open(logo_upload)
            logo = logo.resize((w_image, h_image))  # Resize logo to match image dimensions
            logo = np.array(logo.convert('RGB'))
            
            # Now the logo and image have the same dimensions, so proceed with watermarking
            result = cv2.addWeighted(image_logow, 1, logo, 1, 0)
            
            # Save the result image
            img = Image.fromarray(result, 'RGB')
            uploads_dir = os.path.join(app.root_path, 'static', 'uploads')
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)
            img_path = os.path.join(uploads_dir, 'image.png')
            img.save(img_path)
            full_filename = 'static/uploads/image.png'
            
        else:
            text_mark = request.form['text_mark']
            cv2.putText(image_logow, text=text_mark, org=(w_image - 95, h_image - 10), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5,
                        color=(0,0,255), thickness=2, lineType=cv2.LINE_4)
            img = Image.fromarray(image_logow, 'RGB')
            uploads_dir = os.path.join(app.root_path, 'static', 'uploads')
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)
            img_path = os.path.join(uploads_dir, 'image1.png')
            img.save(img_path)
            full_filename = 'static/uploads/image1.png'

        return render_template('index.html', full_filename=f"{full_filename}?t={timestamp}")

       
# Main function
if __name__ == '__main__':
    app.run(debug=True)
