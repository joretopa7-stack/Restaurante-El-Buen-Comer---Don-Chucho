# Restaurante El Buen Comer - Don Chucho

Sistema web para la gestión e interacción digital del menú y servicios del restaurante **"El Buen Comer"**, desarrollado en Python utilizando el framework Flask y maquetado con Bootstrap 5.3.

## Arquitectura del proyecto

El proyecto implementa la arquitectura **MVC (Modelo-Vista-Controlador)**, estructurada mediante **Blueprints de Flask**. El entorno de desarrollo aísla sus librerías mediante la carpeta del entorno virtual local `.venv`.

### Estructura de carpetas

```
restaurante_el_buen_comer/
├── app/
│   ├── __init__.py               # Fábrica create_app()
│   ├── extensions.py             # db, login_manager, bcrypt (si se usa)
│   ├── models/                   # Capa de datos (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── mesa.py
│   │   ├── plato.py
│   │   ├── pedido.py
│   │   └── detalle_pedido.py
│   ├── services/                 # Lógica de negocio (casos de uso)
│   │   ├── __init__.py
│   │   ├── pedido_service.py
│   │   ├── mesa_service.py
│   │   └── plato_service.py
│   ├── blueprints/               # Módulos por rol (cada uno con sus rutas y templates)
│   │   ├── cliente/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── templates/
│   │   │       ├── index.html
│   │   │       ├── categorias.html
│   │   │       ├── platos.html
│   │   │       ├── detalle_plato.html
│   │   │       ├── seleccionar_mesa.html
│   │   │       └── pedido_cliente.html
│   │   ├── mesero/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── templates/
│   │   │       ├── mesas.html
│   │   │       ├── detalle_mesa.html
│   │   │       └── factura.html
│   │   └── cocina/
│   │       ├── __init__.py
│   │       ├── routes.py
│   │       └── templates/
│   │           ├── ordenes.html
│   │           └── ...
│   ├── static/                   # Recursos estáticos (CSS, JS, imágenes)
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js (opcional)
│   │   └── images/
│   │       ├── categorias/
│   │       └── platos/
│   └── templates/                # Plantillas globales (base, login)
│       ├── base.html
│       └── login.html
├── config.py                     # Configuración (SECRET_KEY, SQLALCHEMY_DATABASE_URI, etc.)
├── requirements.txt              # Dependencias (Flask, Flask-SQLAlchemy, Flask-Login, etc.)
└── run.py                        # Punto de entrada: from app import create_app; app = create_app()
```

## Tecnologías utilizadas

| Tecnología        | Descripción                                                            |
| ----------------- | ---------------------------------------------------------------------- |
| **Python 3.x**    | Lenguaje de programación utilizado dentro del entorno virtual `.venv`. |
| **Flask**         | Framework web para el desarrollo del backend.                          |
| **Jinja2**        | Motor de plantillas para el renderizado de páginas HTML.               |
| **HTML5**         | Estructura de las páginas web.                                         |
| **CSS3**          | Estilos y personalización visual.                                      |
| **Bootstrap 5.3** | Framework utilizado para el maquetado y diseño responsive.             |
| **Git y GitHub**  | Herramientas para el control de versiones y alojamiento del código.    |

## Dependencias instaladas en `.venv`

Todas las librerías necesarias se encuentran instaladas de manera aislada en la carpeta local `.venv`.

| Paquete          | Versión | Descripción                                          |
| ---------------- | ------- | ---------------------------------------------------- |
| **Flask**        | 3.1.x   | Framework web principal.                             |
| **Werkzeug**     | 3.1.x   | Servidor WSGI y manejo de peticiones HTTP.           |
| **Jinja2**       | 3.1.x   | Motor de renderizado de plantillas HTML.             |
| **Click**        | 8.5.x   | Interfaz de línea de comandos para scripts de Flask. |
| **MarkupSafe**   | 3.0.x   | Seguridad y escapado de caracteres en HTML.          |
| **Itsdangerous** | 2.2.x   | Manejo seguro de sesiones y datos firmados.          |
| **Blinker**      | 1.9.x   | Sistema de soporte de eventos para Flask.            |

## Inicialización y ejecución del proyecto

Sigue los siguientes pasos para ejecutar la aplicación haciendo uso de tu entorno virtual `.venv`.

### 1. Clonar el repositorio

```
git clone https://github.com/joretopa7-stack/Restaurante-El-Buen-Comer---Don-Chucho.git
cd Restaurante-El-Buen-Comer---Don-Chucho
```

### 2. Activar el entorno virtual (`.venv`)

Asegúrate de activar siempre el entorno virtual antes de instalar paquetes o ejecutar el servidor.

**En Windows (PowerShell):**

```
.\.venv\Scripts\Activate.ps1
```

**En Windows (CMD):**

```
.\.venv\Scripts\activate.bat
```

**En Linux / macOS:**

```
source .venv/bin/activate
```

> **Nota:** Sabrás que el entorno está activo porque verás `(.venv)` al inicio de la línea de comandos en tu terminal.

### 3. Instalar o verificar dependencias

Con el entorno `(.venv)` activo, instala los requerimientos:

```
pip install -r requirements.txt
```

> **Nota:** Si aún no tienes `requirements.txt`, puedes instalar Flask directamente con:
>
> ```
> pip install flask
> ```

### 4. Ejecutar el servidor de desarrollo

Con el entorno `(.venv)` activo, ejecuta:

```
flask --app app.py run --debug
```

### 5. Abrir la aplicación

Abre tu navegador e ingresa a:

[**http://127.0.0.1:5000**](http://127.0.0.1:5000)

---

## Autor

**Restaurante El Buen Comer - Don Chucho**

Repositorio: [Restaurante El Buen Comer - Don Chucho](https://github.com/joretopa7-stack/Restaurante-El-Buen-Comer---Don-Chucho.git)
