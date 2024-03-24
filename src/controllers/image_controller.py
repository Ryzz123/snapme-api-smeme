from flask import request, jsonify, send_file
from src.services.image_service import ImageService
import io


class ImageController:
    def __init__(self):
        self.service = ImageService()

    def createImageSmeme(self):
        form = request.form
        if 'image' in request.files:
            image = request.files['image']
            data = {
                'header': form.get('header') or '',
                'footer': form.get('footer') or '',
                'watermark': form.get('watermark') or 'snapme'
            }

            if image.filename != '':
                data['image'] = {
                    'name': image.filename,
                    'ext': image.filename.split('.')[-1],
                    'data': image.read(),
                    'size': len(image.read()),
                    'path': f'{image.name}/{image.filename}'
                }
            else:
                data['image'] = ''
        else:
            data = {
                'header': form.get('header') or '',
                'footer': form.get('footer') or '',
                'watermark': form.get('watermark') or 'snapme',
                'image': ''
            }

        response = self.service.createImageSmeme(data)
        if response['status'] == 200 and response['type'] == 'image/png':
            return send_file(io.BytesIO(response['img']), mimetype='image/png')

        return jsonify(response), response['status']
