import os
from flask_restful import Resource, request
from werkzeug import secure_filename
from flask_login import login_required
from flask import session, current_app
from . import api
from .. import ALLOWED_EXTENSIONS

class Upload(Resource):
    decorators = [login_required]

    def post(self):
        my_username = session['user_id']
        user_image = request.files['file']

        app = current_app._get_current_object()

        if user_image and allowed_file(user_image.filename):
            filename = secure_filename(user_image.filename)
            user_image.save(os.path.join(app.config['UPLOAD_FOLDER'], my_username + '.jpg'))
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