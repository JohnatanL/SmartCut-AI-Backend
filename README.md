# SmartCut AI - Backend API REST

API REST desarrollada para gestionar el núcleo de datos del sistema **SmartCut AI**, enfocada en la administración de usuarios, el catálogo de servicios (estilos de corte) y el inventario de productos.

Este proyecto ha sido construido como evidencia académica para el Servicio Nacional de Aprendizaje (SENA) correspondiente a la fase de evaluación **GA4-220501096-AA1-EV01**.

## 🎯 Objetivo del Backend

Proporcionar los servicios base y la persistencia de datos necesarios para operar la lógica de negocio de SmartCut AI. Aunque el frontend de la plataforma incluye interfaces de agenda y previsualización por Inteligencia Artificial, este backend inicial se centra estrictamente en cumplir los requerimientos técnicos de la evidencia, proporcionando operaciones CRUD operativas sobre una base de datos real y protegiendo el acceso mediante autenticación estándar.

## 🛠️ Tecnologías Utilizadas

El stack tecnológico ha sido seleccionado por su rendimiento, simplicidad y tipado fuerte:

* **Lenguaje:** Python 3.12.1

* **Framework Web:** FastAPI (0.104.1)

* **Base de Datos:** SQLite

* **ORM (Mapeo Objeto-Relacional):** SQLAlchemy (2.0.23)

* **Validación de Datos:** Pydantic (2.5.2)

* **Seguridad:** Passlib con Bcrypt (1.7.4) para hashing y Python-JOSE (3.3.0) para tokens JWT.

* **Infraestructura:** Docker, Docker Compose y GitHub Codespaces.

## 📂 Arquitectura y Estructura de Carpetas

El proyecto utiliza una arquitectura modular y plana, priorizando la separación de responsabilidades entre la conexión a base de datos, los modelos físicos, las reglas de validación y la exposición de rutas.

```
smartcut-api-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada y configuración de FastAPI
│   ├── database.py          # Conexión a SQLite y generador de sesiones
│   ├── models.py            # Modelos ORM (SQLAlchemy)
│   ├── schemas.py           # Estructuras de validación JSON (Pydantic)
│   ├── security.py          # Lógica de hashing de contraseñas y firmado JWT
│   └── routers/             # Módulos de endpoints separados por entidad
│       ├── __init__.py
│       ├── auth.py          # Endpoints de inicio y cierre de sesión
│       ├── users.py         # CRUD de Usuarios
│       ├── services.py      # CRUD de Servicios (Catálogo)
│       └── products.py      # CRUD de Productos (Inventario)
├── data/                    # Volumen montado para persistir SQLite (.gitkeep)
├── .env.example             # Plantilla de variables de entorno
├── .gitignore               # Exclusión de binarios, caché y base de datos
├── docker-compose.yml       # Orquestación de contenedores
├── Dockerfile               # Instrucciones de construcción de la imagen
├── requirements.txt         # Dependencias exactas de Python
└── README.md                # Documentación del proyecto

```

## 🗄️ Entidades y Base de Datos

El almacenamiento se realiza en una base de datos relacional **SQLite** (`data/smartcut.db`). Las operaciones se realizan físicamente en el archivo, no en memoria. Se manejan las siguientes entidades principales:

1. **Usuarios (`users`):** Gestiona el personal y los clientes (`id`, `email`, `hashed_password`, `nombre`).

2. **Servicios (`services`):** Representa el catálogo de cortes de cabello disponibles en el negocio (`id`, `nombre`, `descripcion`, `precio`, `duracion_minutos`).

3. **Productos (`products`):** Administra el inventario de artículos de barbería (`id`, `nombre`, `marca`, `precio`, `stock`).

*(Nota: Funcionalidades futuras como el motor de IA o las citas no poseen tablas en esta versión, limitando el alcance a los requerimientos de la fase actual).*

## 🧩 Implementación de Programación Orientada a Objetos (POO)

El proyecto demuestra el uso de POO mediante las siguientes prácticas fundamentales:

* **Modelos ORM (`models.py`):** Las tablas de la base de datos se representan a través de Clases en Python que heredan de la clase base de SQLAlchemy. Los registros son instanciados como objetos.

* **Schemas y Herencia (`schemas.py`):** Pydantic se emplea para definir Clases que modelan la entrada y salida de datos JSON. Se utiliza la herencia de clases (ej. `UserCreate` hereda de `UserBase`) para reutilizar atributos (como `email` y `nombre`) agregando particularidades (como el campo `password` solo en creación), demostrando encapsulamiento y abstracción.

## 🔐 Autenticación y Seguridad

* **Hashing de contraseñas:** Las contraseñas **nunca** se guardan en texto plano. Se procesan a través de la librería Bcrypt en `security.py`, almacenando únicamente un hash unidireccional irrecuperable.

* **Tokens JWT:** Una vez comprobado el hash durante el login, el servidor genera un token JWT **firmado** criptográficamente (no cifrado). Este token asegura la autenticidad de las peticiones subsecuentes.

* **Logout Stateless:** El endpoint `DELETE /auth/logout` cumple el requisito de la matriz de evaluación. Sin embargo, dado que JWT es una arquitectura sin estado (stateless), este endpoint no revoca mágicamente el token en el servidor (al no usar listas de bloqueo para mantener la simplicidad académica); en su lugar, devuelve una instrucción exitosa HTTP 200, delegando la responsabilidad de la eliminación física del token al lado del cliente (Frontend).

## 📡 Endpoints REST

La API expone los cuatro módulos exigidos, aplicando los métodos `GET`, `POST`, `PUT` y `DELETE`. La eliminación de registros se efectúa mediante *borrado físico* sobre la base de datos.

| Módulo | Endpoint | Método | Descripción | 
| ----- | ----- | ----- | ----- | 
| **Auth** | `/auth/login` | `POST` | Verifica credenciales y devuelve un token JWT. | 
| **Auth** | `/auth/verify` | `GET` | Valida el token del header y devuelve el usuario. | 
| **Auth** | `/auth/update-password` | `PUT` | Hashea y actualiza la contraseña del usuario. | 
| **Auth** | `/auth/logout` | `DELETE` | Instruye al cliente para desechar el token JWT. | 
| **Users** | `/users/` | `POST` | Crea un usuario. | 
| **Users** | `/users/` | `GET` | Lista todos los usuarios. | 
| **Users** | `/users/{id}` | `PUT` | Actualiza un usuario específico. | 
| **Users** | `/users/{id}` | `DELETE` | Elimina físicamente a un usuario. | 
| **Services** | `/services/` | `POST` | Crea un estilo de corte. | 
| **Services** | `/services/` | `GET` | Lista el catálogo de servicios. | 
| **Services** | `/services/{id}` | `PUT` | Actualiza precio, descripción, etc. | 
| **Services** | `/services/{id}` | `DELETE` | Elimina un servicio del catálogo. | 
| **Products** | `/products/` | `POST` | Registra un producto de barbería. | 
| **Products** | `/products/` | `GET` | Consulta inventario de productos. | 
| **Products** | `/products/{id}` | `PUT` | Actualiza stock o precio. | 
| **Products** | `/products/{id}` | `DELETE` | Elimina un producto. | 

## ⚙️ Instalación y Ejecución

Puedes ejecutar el proyecto utilizando contenedores Docker (o en GitHub Codespaces) o de forma local con Python.

### Opción 1: Ejecución con Docker o GitHub Codespaces (Recomendado)

El proyecto está diseñado para desplegarse fácilmente utilizando contenedores, asegurando que el entorno sea siempre idéntico y evitando conflictos de versiones.

1. Abre el proyecto en tu entorno de **GitHub Codespaces** o clónalo en tu equipo local con VS Code.

2. Abre la terminal integrada en la raíz del proyecto (`smartcut-api-backend`).

3. Construye e inicia los contenedores ejecutando Docker Compose:

   ```bash
   docker compose up --build -d
   ```

4. Espera a que el proceso termine. El contenedor de la API estará ejecutándose en el puerto `8000`.

   * *En Codespaces:* Ve a la pestaña **Ports** (Puertos), ubica el puerto 8000 y haz clic en el icono del mundo para abrirlo en el navegador.

   * *En Local:* Abre tu navegador en `http://localhost:8000`.

5. **Persistencia de Datos:** La configuración de Docker incluye el volumen `- ./data:/app/data`. Esto garantiza que, aunque el contenedor se apague o reconstruya, la base de datos `smartcut.db` persiste en la carpeta `data/` de tu entorno.

### Opción 2: Ejecución Local Nativa (Python / Uvicorn)

Si prefieres ejecutar la API directamente sin Docker:

1. Crea y activa un entorno virtual de Python (3.12 recomendado):
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux / macOS:
   source venv/bin/activate
   ```

2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

3. (Opcional) Configura tus variables de entorno a partir de la plantilla:
   ```bash
   cp .env.example .env
   ```

4. Inicia el servidor de desarrollo:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

## 🧪 Pruebas con FastAPI Docs (Swagger UI)

FastAPI autogenera la documentación interactiva a través de Swagger UI. No es obligatorio el uso de clientes externos como Postman/Insomnia, ya que la propia interfaz web permite testear los métodos REST.

Para realizar pruebas e interactuar con la base de datos, accede a:
👉 `[URL_DE_TU_PUERTO_8000]/docs`

### Secuencia Práctica de Pruebas

1. **Crear Usuario:** Despliega `POST /users/`, presiona *Try it out*. Envía el JSON con tu `email`, `nombre` y `password`. Obtendrás un Código 201 (Created).

2. **Iniciar Sesión:** Despliega `POST /auth/login`, introduce el email y la contraseña. Al ejecutar, obtendrás una respuesta 200 con el `"access_token"`. Copia ese código sin las comillas.

3. **Autorizar Globalmente:** Sube a la cabecera de la página `/docs` y haz clic en el botón verde **"Authorize"**. Pega el token copiado y haz clic en autorizar. Tu sesión ha iniciado.

4. **Probar Endpoints Protegidos:** Despliega `GET /auth/verify` y ejecútalo. El sistema validará tu token JWT firmado y te devolverá tus datos de usuario (Código 200).

5. **Probar CRUD de Servicios:**

   * Haz un `POST /services/` enviando un JSON (ej. `{"nombre": "Fade Clásico", "descripcion": "Degradado", "precio": 25000, "duracion_minutos": 45}`).

   * Haz un `GET /services/` para confirmar que se insertó en SQLite.

   * Modifícalo con `PUT /services/1`.

   * Elimínalo físicamente con `DELETE /services/1`.

6. **Probar CRUD de Productos:** Realiza la misma operación sobre el módulo `/products/` creando ceras o geles.

## Repositorios relacionados

- **Frontend:** [SmartCut AI Frontend](https://github.com/JohnatanL/SmartCut-AI-Frontend)
