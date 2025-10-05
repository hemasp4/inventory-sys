import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY' ,'supersecretkey')
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL' or 'postgresql://postgres:HEMA5665@localhost:5432/inventory_db')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
