from api.auth_api import api as auth_api
from api.note_api import api as note_api
from api.example_api import api as example_api

def initialize_routes(app):
    app.register_blueprint(note_api, url_prefix='/')
    app.register_blueprint(auth_api, url_prefix='/')
    app.register_blueprint(example_api, url_prefix='/')


