from app import app
from api import initialize_routes

initialize_routes(app)
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')