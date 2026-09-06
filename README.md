#  Documentación del Proyecto - Restaurante El Buen Comer

## 1. Introducción

El sistema **Restaurante El Buen Comer - Don Chucho** es una aplicación web desarrollada en Python con Flask que digitaliza la gestión de un restaurante, ofreciendo tres perfiles de usuario: **Cliente**, **Mesero** y **Cocina**. Permite a los clientes explorar el menú y realizar pedidos, a los meseros gestionar mesas y pedidos, y a la cocina controlar el estado de preparación de los platos.

El objetivo es optimizar la comunicación entre los roles, reduciendo errores y agilizando el servicio.

---

## 2. Características principales

- **Navegación del menú** por categorías y platos con imágenes, descripción y precio.
- **Pedidos por mesa**: los clientes seleccionan su mesa y añaden platos a su pedido.
- **Seguimiento de estado** de cada plato (PEDIDO → ACEPTADO → POR PREPARAR → PREPARANDOSE → TERMINADO → ENTREGADO).
- **Panel del mesero**: visualización de mesas ocupadas/libres, gestión de pedidos (enviar a cocina, cancelar, entregar y facturar).
- **Panel de cocina**: lista de órdenes pendientes con acciones para avanzar en la preparación.
- **Base de datos SQLite** (fácilmente migrable a PostgreSQL/MySQL).
- **Autenticación** mediante sesiones (sin dependencias externas de autenticación).

---

## 3. Tecnologías utilizadas

| Tecnología          | Versión | Propósito                              |
|---------------------|---------|----------------------------------------|
| **Python**          | 3.8+    | Lenguaje de programación principal     |
| **Flask**           | 3.0.x   | Framework web ligero                   |
| **Flask-SQLAlchemy**| 3.1.x   | ORM para la gestión de la base de datos|
| **Jinja2**          | 3.1.x   | Motor de plantillas HTML               |
| **Bootstrap 5**     | 5.3     | Diseño responsive y componentes UI     |
| **SQLite**          | 3       | Base de datos por defecto (embebida)   |
| **Werkzeug**        | 3.0.x   | Utilidades WSGI y seguridad (hashes)   |

---

## 4. Estructura del proyecto

```
restaurante_el_buen_comer/
├── app/
│   ├── __init__.py          # Fábrica de la aplicación y datos iniciales
│   ├── extensions.py        # Instancia de SQLAlchemy
│   ├── models/              # Capa de datos (SQLAlchemy)
│   │   ├── __init__.py      # Agrupa los modelos
│   │   ├── usuario.py       # Tabla de usuarios (mesero/cocina)
│   │   ├── mesa.py          # Tabla de mesas
│   │   ├── plato.py         # Tablas de categorías y platos
│   │   ├── pedido.py        # Tabla de pedidos (cabecera)
│   │   └── detalle_pedido.py# Tabla de líneas de pedido (platos pedidos)
│   ├── services/            # Lógica de negocio (casos de uso)
│   │   ├── __init__.py
│   │   ├── pedido_service.py# Gestión de pedidos y estados
│   │   └── mesa_service.py  # Gestión de mesas
│   ├── blueprints/          # Módulos por rol (controladores y vistas)
│   │   ├── cliente/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py    # Rutas para clientes (menú, pedir, ver pedido)
│   │   │   └── templates/   # Plantillas específicas del cliente
│   │   │       ├── index.html
│   │   │       ├── categorias.html
│   │   │       ├── platos.html
│   │   │       ├── detalle_plato.html
│   │   │       ├── seleccionar_mesa.html
│   │   │       └── pedido_cliente.html
│   │   ├── mesero/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py    # Rutas del mesero (mesas, gestión de pedidos)
│   │   │   └── templates/
│   │   │       ├── mesas.html
│   │   │       ├── detalle_mesa.html
│   │   │       └── factura.html
│   │   └── cocina/
│   │       ├── __init__.py
│   │       ├── routes.py    # Rutas de cocina (órdenes, cambios de estado)
│   │       └── templates/
│   │           └── ordenes.html
│   ├── static/               # Archivos estáticos (CSS, JS, imágenes)
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/               # (vacío por ahora)
│   │   └── images/           # Imágenes de categorías y platos
│   │       ├── categorias/
│   │       └── platos/
│   └── templates/            # Plantillas globales (base y login)
│       ├── base.html
│       └── login.html
├── config.py                 # Configuración de la aplicación
├── requirements.txt          # Dependencias Python
├── run.py                    # Punto de entrada para ejecutar la app
├── restaurante.db            # Base de datos SQLite (se genera al ejecutar)
└── README.md                 # Resumen del proyecto
```

---

## 5. Instalación y configuración

### 5.1. Requisitos previos
- Python 3.8 o superior
- Git (opcional)
- Conexión a Internet para descargar dependencias

### 5.2. Clonar el repositorio
```bash
git clone https://github.com/joretopa7-stack/Restaurante-El-Buen-Comer---Don-Chucho.git
cd Restaurante-El-Buen-Comer---Don-Chucho
```

### 5.3. Crear y activar entorno virtual
**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 5.4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5.5. Configuración
Edita `config.py` si deseas cambiar la base de datos (por defecto usa SQLite). La variable `SECRET_KEY` se puede sobrescribir con una variable de entorno para entornos productivos.

### 5.6. Ejecutar la aplicación
```bash
python run.py
```
La aplicación estará disponible en `http://127.0.0.1:5000`

---

## 6. Uso del sistema

### 6.1. Roles y credenciales
| Rol     | Usuario  | Contraseña |
|---------|----------|------------|
| Mesero  | `mesero1`| `mesero123`|
| Cocina  | `admin`  | `admin123` |

> **Cliente**: no requiere autenticación. Se identifica por su número de mesa.

### 6.2. Flujo de trabajo completo

#### a) Cliente
1. Navega por las categorías y platos.
2. Selecciona un plato y hace clic en **"Pedir este plato"**.
3. Elige su número de mesa (1–4) y confirma.
4. Visualiza su pedido en `/mesa/<num>/pedido`, donde puede ver el estado de cada plato y cancelar aquellos que aún estén en `PEDIDO` o `ACEPTADO`.

#### b) Mesero
1. Inicia sesión con sus credenciales.
2. En el panel de mesas (`/mesero/mesas`), ve las mesas ocupadas y libres.
3. Selecciona una mesa ocupada para ver los platos pedidos.
4. Puede:
   - **Enviar a cocina** (cambia a `ACEPTADO`).
   - **Cancelar** un plato (si aún no se ha entregado).
   - **Entregar** un plato cuando la cocina lo haya terminado (`TERMINADO` → `ENTREGADO`).
5. Cuando la mesa finaliza, hace clic en **"Pedir cuenta"**, lo que genera una factura, calcula el total y libera la mesa.

#### c) Cocina
1. Inicia sesión con sus credenciales.
2. En el panel de órdenes (`/cocina/ordenes`), ve todos los platos con estados `ACEPTADO`, `POR_PREPARAR`, `PREPARANDOSE` o `TERMINADO`.
3. Puede:
   - **Ordenar preparar** (`ACEPTADO` → `POR_PREPARAR`).
   - **Preparándose** (`POR_PREPARAR` → `PREPARANDOSE`).
   - **Terminado** (`PREPARANDOSE` → `TERMINADO`).
   - **Cancelar** un plato en cualquier momento (antes de `ENTREGADO`).

### 6.3. Estados de un plato
| Estado         | Descripción                           | Responsable |
|----------------|---------------------------------------|-------------|
| `PEDIDO`       | Cliente lo ha pedido, pendiente de enviar a cocina | Mesero |
| `ACEPTADO`     | Mesero lo ha enviado a cocina         | Cocina      |
| `POR_PREPARAR` | Cocina ha tomado la orden             | Cocina      |
| `PREPARANDOSE` | Cocina está preparando                | Cocina      |
| `TERMINADO`    | Cocina ha finalizado                  | Mesero      |
| `ENTREGADO`    | Mesero lo ha servido en la mesa       | -           |
| `CANCELADO`    | Cancelado por cliente, mesero o cocina| -           |

---

## 7. Modelos de datos

### 7.1. Diagrama entidad-relación (simplificado)

```
Usuario(id, nombre, password_hash, rol)
Mesa(id, numero, estado)
Categoria(id, key, nombre, imagen)
Plato(id, nombre, precio, acompanamiento, imagen, categoria_id)
Pedido(id, mesa_id, fecha_hora, estado, total)
DetallePedido(id, pedido_id, plato_id, cantidad, estado)
```

**Relaciones:**
- `Pedido.mesa_id` → `Mesa.id` (1:N)
- `Pedido.detalles` → `DetallePedido` (1:N)
- `DetallePedido.plato_id` → `Plato.id` (N:1)
- `Plato.categoria_id` → `Categoria.id` (N:1)

---

## 8. Endpoints principales

| Método | URL                                      | Rol       | Descripción |
|--------|------------------------------------------|-----------|-------------|
| GET    | `/`                                      | Cliente   | Página de bienvenida |
| GET    | `/categorias`                            | Cliente   | Lista de categorías |
| GET    | `/categorias/<cat_key>`                  | Cliente   | Platos de una categoría |
| GET    | `/plato/<int:plato_id>`                  | Cliente   | Detalle del plato |
| GET    | `/pedir/<int:plato_id>`                  | Cliente   | Seleccionar mesa para pedir |
| POST   | `/pedir/<int:plato_id>`                  | Cliente   | Añadir plato al pedido |
| GET    | `/mesa/<int:num_mesa>/pedido`            | Cliente   | Ver estado del pedido |
| GET    | `/cancelar_plato/<int:detalle_id>`       | Cliente   | Cancelar un plato |
| GET    | `/login`                                 | Público   | Formulario de login |
| POST   | `/login`                                 | Público   | Autenticación |
| GET    | `/logout`                                | Público   | Cerrar sesión |
| GET    | `/mesero/mesas`                          | Mesero    | Lista de mesas |
| GET    | `/mesero/mesa/<int:num_mesa>`            | Mesero    | Detalle de una mesa |
| POST   | `/mesero/mesa/<int:num_mesa>/enviar_cocina/<int:detalle_id>` | Mesero | Enviar a cocina |
| POST   | `/mesero/mesa/<int:num_mesa>/cancelar/<int:detalle_id>` | Mesero | Cancelar plato |
| POST   | `/mesero/mesa/<int:num_mesa>/entregar/<int:detalle_id>` | Mesero | Entregar plato |
| GET    | `/mesero/mesa/<int:num_mesa>/cuenta`     | Mesero    | Facturar y liberar mesa |
| GET    | `/cocina/ordenes`                        | Cocina    | Lista de órdenes pendientes |
| POST   | `/cocina/orden/preparar/<int:detalle_id>`| Cocina    | Marcar como preparar |
| POST   | `/cocina/orden/preparando/<int:detalle_id>`| Cocina  | Marcar como preparándose |
| POST   | `/cocina/orden/terminado/<int:detalle_id>`| Cocina   | Marcar como terminado |
| POST   | `/cocina/orden/cancelar/<int:detalle_id>`| Cocina    | Cancelar desde cocina |

---

## 9. Detalles de implementación

### 9.1. Decoradores de autenticación
Cada blueprint define su propio decorador `login_required(rol)` que:
- Verifica que el usuario esté en sesión (`session['usuario_id']`).
- Comprueba que el rol coincida con el requerido.
- Redirige al login si falla.

### 9.2. Servicios
La lógica de negocio reside en la capa de servicios (`PedidoService`, `MesaService`), separada de los controladores. Esto facilita el testing y el mantenimiento.

- `PedidoService.agregar_plato()`: crea o recupera un pedido activo y añade un detalle.
- `PedidoService.cambiar_estado_detalle()`: aplica reglas de transición según el rol.
- `PedidoService.facturar_pedido()`: cierra el pedido y libera la mesa.

### 9.3. Datos iniciales
En `app/__init__.py`, dentro del contexto de la aplicación, se crean automáticamente:
- Usuarios (admin y mesero1)
- Mesas (1 a 4)
- Categorías y platos (según el menú del restaurante)

Esto solo ocurre si las tablas están vacías.

---

## 10. Pruebas y depuración

- El modo debug está activado por defecto (`debug=True` en `run.py`), lo que permite recarga automática y depuración interactiva.
- Para probar el flujo completo, se recomienda abrir tres navegadores o pestañas en modo incógnito para simular cada rol.

---

## 11. Posibles mejoras futuras

- **Migrar a PostgreSQL/MySQL** para entornos productivos.
- **Añadir paginación** en el menú y órdenes.
- **Sistema de notificaciones** en tiempo real (WebSockets) para actualizar estados instantáneamente.
- **Módulo de inventario** para controlar existencias.
- **Múltiples idiomas** (internacionalización).
- **API REST** para integración con aplicaciones móviles.

---

## 12. Contribución

Si deseas contribuir al proyecto:
1. Haz un fork del repositorio.
2. Crea una rama con tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -m "Añade nueva funcionalidad"`).
4. Envía un pull request describiendo los cambios.

---


