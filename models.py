from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db=SQLAlchemy()
mg=Migrate()

class Product(db.Model):
    __tablename__ = "products"
    product_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    movements = db.relationship("ProductMovement", back_populates="product", lazy=True)

class Location(db.Model):
    __tablename__ = "locations"
    location_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    from_movements = db.relationship("ProductMovement", back_populates="from_loc", foreign_keys='ProductMovement.from_location')
    to_movements = db.relationship("ProductMovement", back_populates="to_loc", foreign_keys='ProductMovement.to_location')

class ProductMovement(db.Model):
    __tablename__ = "product_movements"
    movement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    from_location = db.Column(db.String, db.ForeignKey("locations.location_id"), nullable=True)
    to_location = db.Column(db.String, db.ForeignKey("locations.location_id"), nullable=True)
    product_id = db.Column(db.String, db.ForeignKey("products.product_id"), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    product = db.relationship("Product", back_populates="movements")
    from_loc = db.relationship("Location", foreign_keys=[from_location], back_populates="from_movements")
    to_loc = db.relationship("Location", foreign_keys=[to_location], back_populates="to_movements")









