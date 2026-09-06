from app.extensions import db

class DetallePedido(db.Model):
    __tablename__ = 'detalles_pedido'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    plato_id = db.Column(db.Integer, db.ForeignKey('platos.id'), nullable=False)
    cantidad = db.Column(db.Integer, default=1)
    estado = db.Column(db.String(20), default='PEDIDO')
    # Estados: PEDIDO, ACEPTADO, POR_PREPARAR, PREPARANDOSE, TERMINADO, ENTREGADO, CANCELADO

    def __repr__(self):
        return f'<Detalle {self.id} - Plato {self.plato_id} - {self.estado}>'