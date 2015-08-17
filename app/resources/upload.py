import os
from flask_restful import Resource, request
from werkzeug import secure_filename
from flask_login import login_required
from flask import session, current_app
from . import api
from .. import ALLOWED_EXTENSIONS
import PIL
from PIL import Image

class Upload(Resource):
    decorators = [login_required]

    def post(self):
        my_username = session['user_id']
        user_image = request.files['file']

        app = current_app._get_current_object()

        if user_image and allowed_file(user_image.filename):
            filename = secure_filename(user_image.filename)
	    path = os.path.join(app.config['UPLOAD_FOLDER'], my_username + '.jpg')
            user_image.save(path)
	    #resize_image(path)
            return_code = 200
            message = { 'status': 'success', 'message': 'image uploaded successfully.'}

        else:
            return_code = 415
            message = { 'status': 'failure', 'message': 'unsupported file type.'}

        return message, return_code

api.add_resource(Upload, '/upload')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# resize the image to save loading times
def resize_image(image_path):
    basewidth = 500 
    img = Image.open(image_path)
    wpercent = (basewidth/float(img.size[0])) # calculate width %
    hsize = int((float(img.size[1])*float(wpercent))) # calculate height
    exif_flags = img._getexif()
    if exif_flags and exif_flags[274] == 6: # check if image is portrait
        rotate = True
    img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
    if rotate:
        img = img.rotate(-90) 
    img.save(image_path) 
