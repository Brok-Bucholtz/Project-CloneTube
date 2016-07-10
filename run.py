from app.app import app
from app.route import build_route

if __name__ == '__main__':
    build_route(app)
    app.run()
