from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.models import DetallePedido, Pedido, Mesa, Usuario
from app.services.pedido_service import PedidoService

cocina_bp = Blueprint('cocina', __name__, template_folder='templates')

def login_required(rol='cocina'):
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

@cocina_bp.route('/ordenes')
@login_required('cocina')
def ordenes():
    estados_cocina = ['ACEPTADO', 'POR_PREPARAR', 'PREPARANDOSE', 'TERMINADO']
    detalles = DetallePedido.query.filter(DetallePedido.estado.in_(estados_cocina)).all()
    for det in detalles:
        pedido = Pedido.query.get(det.pedido_id)
        mesa = Mesa.query.get(pedido.mesa_id) if pedido else None
        det.num_mesa = mesa.numero if mesa else '?'
    return render_template('ordenes.html', detalles=detalles)

@cocina_bp.route('/orden/preparar/<int:detalle_id>', methods=['POST'])
@login_required('cocina')
def preparar(detalle_id):
    detalle, error = PedidoService.cambiar_estado_detalle(detalle_id, 'POR_PREPARAR', rol='cocina')
    if error:
        flash(error, 'danger')
    else:
        flash('Orden para preparar', 'success')
    return redirect(url_for('cocina.ordenes'))

@cocina_bp.route('/orden/preparando/<int:detalle_id>', methods=['POST'])
@login_required('cocina')
def preparando(detalle_id):
    detalle, error = PedidoService.cambiar_estado_detalle(detalle_id, 'PREPARANDOSE', rol='cocina')
    if error:
        flash(error, 'danger')
    else:
        flash('En preparación', 'success')
    return redirect(url_for('cocina.ordenes'))

@cocina_bp.route('/orden/terminado/<int:detalle_id>', methods=['POST'])
@login_required('cocina')
def terminar(detalle_id):
    detalle, error = PedidoService.cambiar_estado_detalle(detalle_id, 'TERMINADO', rol='cocina')
    if error:
        flash(error, 'danger')
    else:
        flash('Plato terminado', 'success')
    return redirect(url_for('cocina.ordenes'))

@cocina_bp.route('/orden/cancelar/<int:detalle_id>', methods=['POST'])
@login_required('cocina')
def cancelar_cocina(detalle_id):
    detalle, error = PedidoService.cambiar_estado_detalle(detalle_id, 'CANCELADO', rol='cocina')
    if error:
        flash(error, 'danger')
    else:
        flash('Plato cancelado', 'success')
    return redirect(url_for('cocina.ordenes'))