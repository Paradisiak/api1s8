from app import app
from db import db

db.init_app((app))


@app.before_first_request
def create_tables():
    db.create_all()  # Crée les tables qu'il voit dans les imports de app
