from flask import render_template


class App:
    def __init__(self, app):
        self.app = app

    def add_route(self, method, route, controller_class, method_name, middleware_classes=None):
        middleware_classes = middleware_classes or []

        if route == '*':
            route = '/<path:path>'
        else:
            route = route.rstrip('/')

        if not route:
            route = '/'

        def apply_middleware(callback):
            def wrapper(*args, **kwargs):
                for middleware_class in middleware_classes:
                    middleware_instance = middleware_class(self.app)
                    middleware_instance.before_request()
                return callback(*args, **kwargs)

            return wrapper

        controller_instance = controller_class()

        endpoint = route + '.' + method_name

        @self.app.route(route, methods=[method], endpoint=endpoint)
        @apply_middleware
        def execute_controller(*args, **kwargs):
            controller_method = getattr(controller_instance, method_name, None)
            if controller_method:
                return controller_method(*args, **kwargs)
            else:
                return render_template('404.html', models={'title': 'Page Not Found'})
