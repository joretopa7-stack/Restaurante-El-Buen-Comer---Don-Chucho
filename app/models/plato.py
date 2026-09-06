from app.extensions import db

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.String(200))

    platos = db.relationship('Plato', backref='categoria', lazy=True)

class Plato(db.Model):
    __tablename__ = 'platos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    acompanamiento = db.Column(db.String(200))
    imagen = db.Column(db.String(200))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)

    detalles = db.relationship('DetallePedido', backref='plato', lazy=True)