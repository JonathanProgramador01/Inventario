import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    contraseña = db.Column(db.String(120), nullable=False)
    rol = db.Column(db.String(50), nullable=False, default='miembro')  # admin, veterano, miembro

class Almacen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    unidad = db.Column(db.String(50))  # Ej: kilos, piezas, litros


class Entrada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    almacen_id = db.Column(db.Integer, db.ForeignKey('almacen.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime)

    producto = db.relationship('Producto')
    almacen = db.relationship('Almacen')


class Salida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    almacen_id = db.Column(db.Integer, db.ForeignKey('almacen.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime)

    producto = db.relationship('Producto')
    almacen = db.relationship('Almacen')


class Existencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    almacen_id = db.Column(db.Integer, db.ForeignKey('almacen.id'), nullable=False)
    cantidad_actual = db.Column(db.Float, nullable=False)

    producto = db.relationship('Producto')
    almacen = db.relationship('Almacen')


