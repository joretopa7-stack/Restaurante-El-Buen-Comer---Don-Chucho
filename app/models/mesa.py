from app.extensions import db

class Mesa(db.Model):
    __tablename__ = 'mesas'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    estado = db.Column(db.String(20), default='libre')  # 'libre' o 'ocupada'

    pedidos = db.relationship('Pedido', backref='mesa', lazy=True)

    def __repr__(self):
        return f'<Mesa {self.numero} - {self.estado}>'