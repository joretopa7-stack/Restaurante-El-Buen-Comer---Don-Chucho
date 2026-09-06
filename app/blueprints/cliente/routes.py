from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Categoria, Plato, Mesa, Usuario
from app.services.pedido_service import PedidoService
from app.services.mesa_service import MesaService

cliente_bp = Blueprint('cliente', __name__, template_folder='templates')

def login_required(rol=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'usuario_id' not in session:
                flash('Debes iniciar sesión', 'warning')
                return redirect(url_for('cliente.login'))
            if rol:
                usuario = Usuario.query.get(session['usuario_id'])
                if not usuario or usuario.rol != rol:
                    flash('No tienes permiso para acceder', 'danger')
                    return redirect(url_for('cliente.index'))
            return f(*args, **kwargs)
        return decorated
    return decorator

@cliente_bp.route('/')
def index():
    return render_template('index.html')

@cliente_bp.route('/categorias')
def categorias():
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=categorias)

@cliente_bp.route('/categorias/<cat_key>')
def platos(cat_key):
    categoria = Categoria.query.filter_by(key=cat_key).first_or_404()
    platos = Plato.query.filter_by(categoria_id=categoria.id).all()
    return render_template('platos.html', categoria=categoria, platos=platos)

@cliente_bp.route('/plato/<int:plato_id>')
def detalle_plato(plato_id):
    plato = Plato.query.get_or_404(plato_id)
    return render_template('detalle_plato.html', plato=plato)

@cliente_bp.route('/pedir/<int:plato_id>', methods=['GET', 'POST'])
def pedir_plato(plato_id):
    plato = Plato.query.get_or_404(plato_id)
    if request.method == 'POST':
        num_mesa = request.form.get('num_mesa', type=int)
        if not num_mesa:
            flash('Debes ingresar un número de mesa', 'danger')
            return redirect(url_for('cliente.pedir_plato', plato_id=plato_id))
        mesa = Mesa.query.filter_by(numero=num_mesa).first()
        if not mesa:
            flash('Mesa no encontrada', 'danger')
            return redirect(url_for('cliente.pedir_plato', plato_id=plato_id))
        detalle, error = PedidoService.agregar_plato(num_mesa, plato_id)
        if error:
            flash(error, 'danger')
        else:
            flash(f'Plato {plato.nombre} agregado al pedido de la mesa {num_mesa}', 'success')
        return redirect(url_for('cliente.ver_pedido', num_mesa=num_mesa))
    mesas = Mesa.query.all()
    return render_template('seleccionar_mesa.html', plato=plato, mesas=mesas)

@cliente_bp.route('/mesa/<int:num_mesa>/pedido')
def ver_pedido(num_mesa):
    pedido = PedidoService.obtener_pedido_activo(num_mesa)
    if not pedido:
        return render_template('pedido_cliente.html', mesa=None, detalles=[], total=0)
    detalles = PedidoService.obtener_detalles_con_plato(pedido)
    total = pedido.calcular_total()
    mesa = Mesa.query.filter_by(numero=num_mesa).first()
    return render_template('pedido_cliente.html', mesa=mesa, detalles=detalles, total=total)

@cliente_bp.route('/cancelar_plato/<int:detalle_id>')
def cancelar_plato(detalle_id):
    detalle, error = PedidoService.cambiar_estado_detalle(detalle_id, 'CANCELADO', rol='cliente')
    if error:
        flash(error, 'danger')
    else:
        flash('Plato cancelado', 'success')
    pedido = detalle.pedido if detalle else None
    if pedido:
        mesa = Mesa.query.get(pedido.mesa_id)
        return redirect(url_for('cliente.ver_pedido', num_mesa=mesa.numero))
    return redirect(url_for('cliente.index'))

@cliente_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        usuario = Usuario.query.filter_by(nombre=username).first()
        if usuario and usuario.check_password(password):
            session['usuario_id'] = usuario.id
            session['rol'] = usuario.rol
            flash('Inicio de sesión exitoso', 'success')
            if usuario.rol == 'mesero':
                return redirect(url_for('mesero.mesas'))
            elif usuario.rol == 'cocina':
                return redirect(url_for('cocina.ordenes'))
            else:
                return redirect(url_for('cliente.index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

@cliente_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('cliente.index'))