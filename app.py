from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db,mg
from routes import main



def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mg.init_app(app,db)
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
    return app




if __name__ == "__main__":
    app=create_app()
    app.run(debug=True,port=5000,host="0.0.0.0")
    