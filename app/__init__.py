from flask import Flask, jsonify
from flask_migrate import Migrate
from config import Config

from app.db import db
from app.auth import token_required, auth_bp
from app.routes import bp as routes_bp

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config['SECRET_KEY'] = 'your-secret-key'

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'message': 'Bad Request'}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'message': 'Unauthorized'}), 401

    @app.errorhandler(404)
    def bad_request(error):
        return jsonify({'message': 'Not found'}), 404

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({'message': 'Internal server error'}), 500

    @app.errorhandler(503)
    def bad_request(error):
        return jsonify({'message': 'Server unavailable'}), 503

    return app