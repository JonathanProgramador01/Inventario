from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from app import app




class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)



















with app.app_context():
    db.create_all()
