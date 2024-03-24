from flask import request, send_file, jsonify, render_template
import os


class UtilityController:
    @staticmethod
    def index():
        return render_template('home/index.html', models={'title': 'Home'})

    @staticmethod
    def notfound(path):
        return jsonify({'message': f'Invalid route {path}'}), 404

    @staticmethod
    def image():
        name_file = request.args.get('name')

        public_folder = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../public'))
        images_folder = os.path.normpath(os.path.join(public_folder, 'images'))
        image_path = os.path.join(images_folder, name_file)

        _, file_extension = os.path.splitext(name_file)
        mimetype = 'image/jpeg' if file_extension.lower() in ['.jpg', '.jpeg'] else 'image/png'

        return send_file(image_path, mimetype=mimetype)

    @staticmethod
    def css():
        name_file = request.args.get('name')

        public_folder = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../public'))
        css_folder = os.path.normpath(os.path.join(public_folder, 'css'))
        css_path = os.path.join(css_folder, name_file)

        return send_file(css_path, mimetype='text/css')

    @staticmethod
    def js():
        name_file = request.args.get('name')

        public_folder = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../public'))
        js_folder = os.path.normpath(os.path.join(public_folder, 'js'))
        js_path = os.path.join(js_folder, name_file)

        return send_file(js_path, mimetype='text/javascript')
