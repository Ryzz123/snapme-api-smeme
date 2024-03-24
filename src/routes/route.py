from src.controllers.utility_controller import UtilityController
from src.controllers.image_controller import ImageController


class Route:
    def __init__(self, app):
        routes = {
            'home': {
                'routes': [
                    ('GET', '/', UtilityController, 'index', []),
                ]
            },
            'api': {
                'routes': [
                    ('POST', '/api/smeme', ImageController, 'createImageSmeme', []),
                ]
            },
            'utils': {
                'routes': [
                    ('GET', '*', UtilityController, 'notfound', []),
                ]
            },
            'utility': {
                'routes': [
                    ('GET', '/public/images', UtilityController, 'image', []),
                    ('GET', '/public/css', UtilityController, 'css', []),
                    ('GET', '/public/js', UtilityController, 'js', []),
                ]
            },
        }

        for group_name, group_data in routes.items():
            for method, path, controller, action, middlewares in group_data['routes']:
                app.add_route(method, path, controller, action, middlewares)
