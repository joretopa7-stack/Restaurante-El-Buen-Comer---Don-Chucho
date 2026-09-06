from app.extensions import db
from datetime import datetime

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    mesa_id = db.Column(db.Integer, db.ForeignKey('mesas.id'), nullable=False)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='ACTIVO')  # 'ACTIVO', 'FACTURADO', 'CANCELADO'
    total = db.Column(db.Integer, default=0)

    detalles = db.relationship('DetallePedido', backref='pedido', lazy=True)

    def calcular_total(self):
        total = 0
        for detalle in self.detalles:
            if detalle.estado != 'CANCELADO':
                total += detalle.cantidad * detalle.plato.precio
        self.total = total
        return total

    def __repr__(self):
        return f'<Pedido {self.id} - Mesa {self.mesa_id}>'