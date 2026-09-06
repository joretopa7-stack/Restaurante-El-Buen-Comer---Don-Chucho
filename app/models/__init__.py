from .usuario import Usuario
from .mesa import Mesa
from .plato import Plato, Categoria
from .pedido import Pedido
from .detalle_pedido import DetallePedido

def init_data():
    """Carga datos por defecto si la base de datos está vacía."""
    from app.extensions import db
    from app.models import Usuario, Mesa, Categoria, Plato, Pedido, DetallePedido

    if Usuario.query.count() == 0:
        # Usuarios
        admin = Usuario(nombre='admin', rol='cocina')
        admin.set_password('admin123')
        mesero = Usuario(nombre='mesero1', rol='mesero')
        mesero.set_password('mesero123')
        db.session.add_all([admin, mesero])
        db.session.commit()

    if Mesa.query.count() == 0:
        for i in range(1, 5):
            mesa = Mesa(numero=i, estado='libre')
            db.session.add(mesa)
        db.session.commit()

    if Categoria.query.count() == 0:
        categorias_data = [
            ('pescados', 'Pescados', 'categorias/pescados.jpg'),
            ('carnes', 'Carnes', 'categorias/carnes.jpg'),
            ('pastas', 'Pastas', 'categorias/pastas.jpg'),
            ('platos_tipicos', 'Platos Típicos', 'categorias/platos_tipicos.jpg'),
            ('sopas', 'Sopas', 'categorias/sopas.jpg'),
            ('bebidas', 'Bebidas', 'categorias/bebidas.jpg')
        ]
        for key, nombre, imagen in categorias_data:
            cat = Categoria(key=key, nombre=nombre, imagen=imagen)
            db.session.add(cat)
        db.session.commit()

    if Plato.query.count() == 0:
        platos_data = {
            'pescados': [
                ('Cazuela de Mariscos', 35000, 'Arroz de coco y patacones', 'platos/cazuela_mariscos.jpg'),
                ('Pargo Rojo Frito', 32000, 'Ensalada fresca y yuca', 'platos/pargo_rojo.jpg')
            ],
            'carnes': [
                ('Lomo al Trapo', 38000, 'Papa al horno y ensalada mixta', 'platos/lomo_trapo.jpg')
            ],
            'pastas': [
                ('Lasagna de Carne', 25000, 'Pan con ajo y queso parmesano', 'platos/lasagna.jpg')
            ],
            'platos_tipicos': [
                ('Bandeja Paisa', 30000, 'Arroz, frijol, huevo, chicharrón, aguacate', 'platos/bandeja_paisa.jpg')
            ],
            'sopas': [
                ('Ajiaco Santafereño', 22000, 'Pollo, alcaparras, crema de leche y mazorca', 'platos/ajiaco.jpg')
            ],
            'bebidas': [
                ('Limonada de Coco', 8000, 'Hielo y rodaja de limón', 'platos/limonada_coco.jpg')
            ]
        }
        for cat_key, platos in platos_data.items():
            categoria = Categoria.query.filter_by(key=cat_key).first()
            if categoria:
                for nombre, precio, acompanamiento, imagen in platos:
                    plato = Plato(
                        nombre=nombre,
                        precio=precio,
                        acompanamiento=acompanamiento,
                        imagen=imagen,
                        categoria_id=categoria.id
                    )
                    db.session.add(plato)
        db.session.commit()