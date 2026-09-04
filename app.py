from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta_don_chucho'

# Base de datos simulada del restaurante "El Buen Comer"
CATEGORIAS = {
    'pescados': {'nombre': 'Pescados', 'imagen': 'categorias/pescados.jpg'},
    'carnes': {'nombre': 'Carnes', 'imagen': 'categorias/carnes.jpg'},
    'pastas': {'nombre': 'Pastas', 'imagen': 'categorias/pastas.jpg'},
    'platos_tipicos': {'nombre': 'Platos Típicos', 'imagen': 'categorias/platos_tipicos.jpg'},
    'sopas': {'nombre': 'Sopas', 'imagen': 'categorias/sopas.jpg'},
    'bebidas': {'nombre': 'Bebidas', 'imagen': 'categorias/bebidas.jpg'}
}

PLATOS = {
    'pescados': [
        {'id': 1, 'nombre': 'Cazuela de Mariscos', 'precio': 35000, 'acompanamiento': 'Arroz de coco y patacones', 'imagen': 'platos/cazuela_mariscos.jpg'},
        {'id': 2, 'nombre': 'Pargo Rojo Frito', 'precio': 32000, 'acompanamiento': 'Ensalada fresca y yuca', 'imagen': 'platos/pargo_rojo.jpg'}
    ],
    'carnes': [
        {'id': 3, 'nombre': 'Lomo al Trapo', 'precio': 38000, 'acompanamiento': 'Papa al horno y ensalada mixta', 'imagen': 'platos/lomo_trapo.jpg'}
    ],
    'pastas': [
        {'id': 4, 'nombre': 'Lasagna de Carne', 'precio': 25000, 'acompanamiento': 'Pan con ajo y queso parmesano', 'imagen': 'platos/lasagna.jpg'}
    ],
    'platos_tipicos': [
        {'id': 5, 'nombre': 'Bandeja Paisa', 'precio': 30000, 'acompanamiento': 'Arroz, frijol, huevo, chicharrón, aguacate', 'imagen': 'platos/bandeja_paisa.jpg'}
    ],
    'sopas': [
        {'id': 6, 'nombre': 'Ajiaco Santafereño', 'precio': 22000, 'acompanamiento': 'Pollo, alcaparras, crema de leche y mazorca', 'imagen': 'platos/ajiaco.jpg'}
    ],
    'bebidas': [
        {'id': 7, 'nombre': 'Limonada de Coco', 'precio': 8000, 'acompanamiento': 'Hielo y rodaja de limón', 'imagen': 'platos/limonada_coco.jpg'}
    ]
}

@app.route('/')
def bienvenida():
    return render_template('bienvenida.html')

@app.route('/categorias')
def categorias():
    return render_template('categorias.html', categorias=CATEGORIAS)

@app.route('/categorias/<cat_key>')
def platos(cat_key):
    categoria = CATEGORIAS.get(cat_key)
    lista_platos = PLATOS.get(cat_key, [])
    return render_template('platos.html', categoria=categoria, platos=lista_platos)

@app.route('/plato/<int:plato_id>')
def detalle_plato(plato_id):
    plato_encontrado = None
    for lista in PLATOS.values():
        for p in lista:
            if p['id'] == plato_id:
                plato_encontrado = p
                break
    return render_template('detalle_plato.html', plato=plato_encontrado)

@app.route('/agregar_al_pedido/<int:plato_id>', methods=['POST'])
def agregar_al_pedido(plato_id):
    if 'pedido' not in session:
        session['pedido'] = []
    
    plato_encontrado = None
    for lista in PLATOS.values():
        for p in lista:
            if p['id'] == plato_id:
                plato_encontrado = p
                break

    if plato_encontrado:
        session['pedido'].append(plato_encontrado)
        session.modified = True

    return redirect(url_for('ver_pedido'))

@app.route('/pedido')
def ver_pedido():
    pedido = session.get('pedido', [])
    total = sum(p['precio'] for p in pedido)
    return render_template('pedido.html', pedido=pedido, total=total)

@app.route('/limpiar_pedido')
def limpiar_pedido():
    session.pop('pedido', None)
    return redirect(url_for('categorias'))

if __name__ == '__main__':
    app.run(debug=True)
