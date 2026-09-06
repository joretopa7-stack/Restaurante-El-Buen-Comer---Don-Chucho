from app.models import Mesa

class MesaService:
    @staticmethod
    def obtener_todas():
        return Mesa.query.order_by(Mesa.numero).all()

    @staticmethod
    def obtener_por_numero(numero):
        return Mesa.query.filter_by(numero=numero).first()

    @staticmethod
    def cambiar_estado(mesa_id, nuevo_estado):
        mesa = Mesa.query.get(mesa_id)
        if mesa:
            mesa.estado = nuevo_estado
            from app.extensions import db
            db.session.commit()
        return mesa