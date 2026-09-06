from app.extensions import db
from app.models import Pedido, DetallePedido, Mesa, Plato

class PedidoService:

    @staticmethod
    def obtener_o_crear_pedido(mesa_numero):
        mesa = Mesa.query.filter_by(numero=mesa_numero).first()
        if not mesa:
            return None, "Mesa no encontrada"
        pedido = Pedido.query.filter_by(mesa_id=mesa.id, estado='ACTIVO').first()
        if not pedido:
            pedido = Pedido(mesa_id=mesa.id)
            db.session.add(pedido)
            mesa.estado = 'ocupada'
            db.session.commit()
        return pedido, None

    @staticmethod
    def agregar_plato(mesa_numero, plato_id, cantidad=1):
        pedido, error = PedidoService.obtener_o_crear_pedido(mesa_numero)
        if error:
            return None, error
        plato = Plato.query.get(plato_id)
        if not plato:
            return None, "Plato no encontrado"
        detalle = DetallePedido(
            pedido_id=pedido.id,
            plato_id=plato_id,
            cantidad=cantidad,
            estado='PEDIDO'
        )
        db.session.add(detalle)
        db.session.commit()
        pedido.calcular_total()
        db.session.commit()
        return detalle, None

    @staticmethod
    def cambiar_estado_detalle(detalle_id, nuevo_estado, rol=None):
        detalle = DetallePedido.query.get(detalle_id)
        if not detalle:
            return None, "Detalle no encontrado"

        # Validaciones según el rol
        if rol == 'cliente':
            if detalle.estado not in ['PEDIDO', 'ACEPTADO']:
                return None, "No puedes cancelar un plato que ya está en preparación"
            if nuevo_estado != 'CANCELADO':
                return None, "Los clientes solo pueden cancelar"
        elif rol == 'mesero':
            transiciones = {
                'PEDIDO': ['ACEPTADO', 'CANCELADO'],
                'TERMINADO': ['ENTREGADO'],
                'ACEPTADO': ['CANCELADO'],
                'POR_PREPARAR': ['CANCELADO'],
                'PREPARANDOSE': ['CANCELADO']
            }
            if nuevo_estado not in transiciones.get(detalle.estado, []):
                return None, f"No puedes cambiar de {detalle.estado} a {nuevo_estado}"
        elif rol == 'cocina':
            if detalle.estado == 'ACEPTADO' and nuevo_estado != 'POR_PREPARAR':
                return None, "Debes ordenar preparar primero"
            if detalle.estado == 'POR_PREPARAR' and nuevo_estado not in ['PREPARANDOSE', 'CANCELADO']:
                return None, "Solo puedes pasar a preparándose o cancelar"
            if detalle.estado == 'PREPARANDOSE' and nuevo_estado not in ['TERMINADO', 'CANCELADO']:
                return None, "Solo puedes terminar o cancelar"
            if detalle.estado == 'TERMINADO' and nuevo_estado != 'CANCELADO':
                return None, "Ya terminado, solo puede cancelar"
        else:
            return None, "Rol no válido"

        detalle.estado = nuevo_estado
        db.session.commit()
        # Actualizar total del pedido
        pedido = Pedido.query.get(detalle.pedido_id)
        pedido.calcular_total()
        db.session.commit()
        return detalle, None

    @staticmethod
    def obtener_pedido_activo(mesa_numero):
        mesa = Mesa.query.filter_by(numero=mesa_numero).first()
        if not mesa:
            return None
        return Pedido.query.filter_by(mesa_id=mesa.id, estado='ACTIVO').first()

    @staticmethod
    def obtener_detalles_con_plato(pedido):
        if not pedido:
            return []
        from sqlalchemy.orm import joinedload
        return DetallePedido.query.filter_by(pedido_id=pedido.id).options(joinedload(DetallePedido.plato)).all()

    @staticmethod
    def facturar_pedido(mesa_numero):
        mesa = Mesa.query.filter_by(numero=mesa_numero).first()
        if not mesa:
            return None, "Mesa no encontrada"
        pedido = Pedido.query.filter_by(mesa_id=mesa.id, estado='ACTIVO').first()
        if not pedido:
            return None, "No hay pedido activo"
        pedido.estado = 'FACTURADO'
        mesa.estado = 'libre'
        db.session.commit()
        return pedido, None