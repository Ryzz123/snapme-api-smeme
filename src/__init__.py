from src.app.app import App
from src.routes.route import Route

app = App(__name__)
Route(app)
