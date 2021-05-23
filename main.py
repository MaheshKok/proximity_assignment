# -*- coding: utf-8 -*-

# Create the Flask application
from application.app import create_web_app

app = create_web_app()

if __name__ == "__main__":
    # Start application
    app.run(debug=True)
