from application import constants


def register_database(app):
    from application.extensions import db

    # Initialize SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = constants.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.init_app(app)

    with app.app_context():
        db.create_all()
