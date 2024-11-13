from flask import Flask
from database import init_db, db
from routes import register_routes

app = Flask(__name__)

# Initialize the database
init_db(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Register the routes
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
