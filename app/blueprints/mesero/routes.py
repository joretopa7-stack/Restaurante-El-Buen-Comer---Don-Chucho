from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, abort, session
from app.models import Mesa, Usuario
from app.services.pedido_service import PedidoService
from app.services.mesa_service import MesaService

mesero_bp = Blueprint('mesero', __name__, template_folder='templates')

def login_required(rol='mesero'):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'usuario_id' not in session:
                flash('Debes iniciar sesión', 'warning')
                return redirect(url_for('cliente.login'))
            usuario = Usuario.query.get(session['usuario_id'])
            if not usuario or usuario.rol != rol:
                flash('No tienes permiso para acceder', 'danger')
                return redirect(url_for('cliente.index'))
            return f(*args, **kwargs)
        return decorated
    return decorator

@mesero_bp.route('/mesas')
@login_required('mesero')
def mesas():
    mesas = MesaService.obtener_todas()
    return render_template('mesas.html', mesas=mesas)

@mesero_bp.route('/mesa/<int:num_mesa>')
@login_required('mesero')
def detalle_mesa(num_mesa):
    mesa = MesaService.obtener_por_numero(num_mesa)
    if not mesa:
        abort(404)
    pedido = PedidoService.obtener_pedido_activo(num_mesa)
    detalles = []
    total = 0
    if pedido:
        detalles = PedidoService.obtener_detalles_con_plato(pedido)
        total = pedido.calcular_total()
    return render_template('detalle_mesa.html', mesa=mesa, detalles=detalles, total=total)

@mesero_bp.route('/mesa/<int:num_mesa>/enviar_cocina/<int:detalle_id>', methods=['POST'])
@login_required('mesero')
def enviar_cocina(num_mesa, detalle_id):
    detalle, error = PedidoService.cambiar_estado_detalle(detalle_id, 'ACEPTADO', rol='mesero')
    if error:
        flash(error, 'danger')
    else:
        flash('Enviado a cocina', 'success')
    return redirect(url_for('mesero.detalle_mesa', num_mesa=num_mesa))

@mesero_bp.route('/mesa/<int:num_mesa>/cancelar/<int:detalle_id>', methods=['POST'])
@login_required('mesero')
def cancelar_detalle(num_mesa, detalle_id):
    detalle, error = PedidoService.cambiar_estado_detalle(detalle_id, 'CANCELADO', rol='mesero')
    if error:
        flash(error, 'danger')
    else:
        flash('Plato cancelado', 'success')
    return redirect(url_for('mesero.detalle_mesa', num_mesa=num_mesa))

@mesero_bp.route('/mesa/<int:num_mesa>/entregar/<int:detalle_id>', methods=['POST'])
@login_required('mesero')
def entregar_detalle(num_mesa, detalle_id):
    detalle, error = PedidoService.cambiar_estado_detalle(detalle_id, 'ENTREGADO', rol='mesero')
    if error:
        flash(error, 'danger')
    else:
        flash('Plato entregado', 'success')
    return redirect(url_for('mesero.detalle_mesa', num_mesa=num_mesa))

@mesero_bp.route('/mesa/<int:num_mesa>/cuenta')
@login_required('mesero')
def pedir_cuenta(num_mesa):
    pedido, error = PedidoService.facturar_pedido(num_mesa)
    if error:
        flash(error, 'danger')
        return redirect(url_for('mesero.detalle_mesa', num_mesa=num_mesa))
    detalles = PedidoService.obtener_detalles_con_plato(pedido)
    total = pedido.total
    mesa = MesaService.obtener_por_numero(num_mesa)
    return render_template('factura.html', mesa=mesa, detalles=detalles, total=total)