# 🛡️ SecureAuth Backend

🇪🇸 Versión en español · 🇬🇧 English version below ⬇️

API backend de autenticación y control de acceso, construida con **FastAPI**, **SQLAlchemy** y **SQL Server** (en contenedores Docker), siguiendo una arquitectura limpia y principios de **Domain-Driven Design (DDD)**.

Es un proyecto de portafolio que aplica buenas prácticas de seguridad usadas en entornos de producción: sesiones controladas, roles, protección contra fuerza bruta y registro de auditoría.

## 🚀 Características

- **Autenticación con cookies seguras:** cookies `HttpOnly`, `Secure` y `SameSite=Lax`. `HttpOnly` reduce el riesgo de robo del token mediante XSS, y `SameSite=Lax` ayuda a mitigar ataques CSRF.
- **Sesión única (`jti`):** cada token tiene un identificador único que se valida contra la base de datos.
- **Control de acceso basado en roles (RBAC):** los endpoints administrativos (`/admin/*`) exigen privilegios de administrador.
- **Protección contra fuerza bruta:** límite de peticiones con `slowapi` en las rutas críticas de autenticación (5 peticiones por minuto).
- **Registro de auditoría:** se guardan en la base de datos las acciones importantes y la IP de origen del cliente (`AuditLogModel`).
- **Manejo global de excepciones:** controladores centralizados para errores de base de datos (`pyodbc`) y errores internos del servidor.
- **Contraseñas con hash:** se almacenan con bcrypt (a través de Passlib), nunca en texto plano.
- **JWT firmado:** los tokens se firman para detectar modificaciones (un JWT firmado no está cifrado: no guardes datos sensibles en su contenido).

## 🛠️ Stack tecnológico

| Componente | Uso |
|---|---|
| Python 3.11+ | Lenguaje |
| FastAPI | Framework web asíncrono |
| SQLAlchemy + pyodbc | ORM y conector para SQL Server (aislamiento `READ COMMITTED`) |
| Docker + SQL Server | Base de datos relacional persistente |
| Pydantic | Validación y tipado de entrada y salida |
| Passlib (bcrypt) | Hash de contraseñas |
| SlowAPI | Límite de peticiones (rate limiting) |
| Python-Jose | Creación y validación de JWT firmados |

## 📂 Estructura del proyecto

```text
SecureAuth/
├── domain/           # Entidades de dominio y lógica de negocio
├── infrastructure/   # Persistencia, modelos y seguridad (JWT, jti, auditoría)
├── schema/           # Esquemas Pydantic de entrada y salida
├── main.py           # Rutas, middleware de seguridad y manejo de errores
├── requirements.txt  # Dependencias
└── README.md         # Documentación
```

> El archivo `.env` con los secretos **no se sube al repositorio**.

## ⚙️ Instalación

**Requisitos previos:** Python 3.11+, Docker, Git y el *ODBC Driver for SQL Server* (necesario para `pyodbc`).

```bash
# 1. Clonar el repositorio
git clone https://github.com/Felipe-cyberpunk/SecureAuth.git
cd SecureAuth

# 2. Crear y activar un entorno virtual
python -m venv venv
# Linux / macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

**4. Levantar SQL Server con Docker** (ejemplo, ajústalo a tu configuración):

```bash
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=<TuContraseñaSegura>" \
  -p 1433:1433 --name sqlserver -d mcr.microsoft.com/mssql/server:2022-latest
```

**5. Configurar las variables de entorno** creando un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=una_clave_secreta_larga_y_aleatoria
# Agrega aquí las variables de conexión a tu base de datos
# (usuario, contraseña, servidor, nombre de la base)
```

## ▶️ Ejecución

```bash
uvicorn main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 🧭 Estado del proyecto y próximos pasos

Proyecto de portafolio y aprendizaje, que no ha sido auditado por terceros.

- [ ] Migrar de `python-jose` a `PyJWT` (librería con mantenimiento activo)
- [ ] Agregar `docker-compose.yml` para levantar la API y la base de datos con un solo comando
- [ ] Agregar pruebas automatizadas
- [ ] Agregar `.env.example`
- [ ] Capturas de pantalla de `/docs`

---

# 🛡️ SecureAuth Backend (English)

A backend API for authentication and access control, built with **FastAPI**, **SQLAlchemy** and **SQL Server** (running in Docker), following a clean architecture and **Domain-Driven Design (DDD)** principles.

It is a portfolio project that applies security practices commonly used in production environments: controlled sessions, roles, brute-force protection and audit logging.

## 🚀 Features

- **Secure cookie-based authentication:** `HttpOnly`, `Secure` and `SameSite=Lax` cookies. `HttpOnly` reduces the risk of token theft through XSS, and `SameSite=Lax` helps mitigate CSRF attacks.
- **Single session (`jti`):** every token carries a unique identifier that is validated against the database.
- **Role-Based Access Control (RBAC):** administrative endpoints (`/admin/*`) require admin privileges.
- **Brute-force protection:** request rate limiting with `slowapi` on critical authentication routes (5 requests per minute).
- **Audit logging:** important actions and the client's IP address are stored in the database (`AuditLogModel`).
- **Global exception handling:** centralized handlers for database errors (`pyodbc`) and internal server errors.
- **Hashed passwords:** stored with bcrypt (via Passlib), never in plain text.
- **Signed JWT:** tokens are signed so tampering can be detected (a signed JWT is not encrypted: do not store sensitive data in its payload).

## 🛠️ Technology stack

| Component | Purpose |
|---|---|
| Python 3.11+ | Language |
| FastAPI | Async web framework |
| SQLAlchemy + pyodbc | ORM and SQL Server connector (`READ COMMITTED` isolation) |
| Docker + SQL Server | Persistent relational database |
| Pydantic | Input and output validation and typing |
| Passlib (bcrypt) | Password hashing |
| SlowAPI | Rate limiting |
| Python-Jose | Signed JWT creation and validation |

## 📂 Project structure

```text
SecureAuth/
├── domain/           # Domain entities and business logic
├── infrastructure/   # Persistence, models and security (JWT, jti, auditing)
├── schema/           # Pydantic input/output schemas
├── main.py           # Routes, security middleware and error handling
├── requirements.txt  # Dependencies
└── README.md         # Documentation
```

> The `.env` file with secrets is **not committed** to the repository.

## ⚙️ Installation

**Prerequisites:** Python 3.11+, Docker, Git and the *ODBC Driver for SQL Server* (required by `pyodbc`).

```bash
# 1. Clone the repository
git clone https://github.com/Felipe-cyberpunk/SecureAuth.git
cd SecureAuth

# 2. Create and activate a virtual environment
python -m venv venv
# Linux / macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

**4. Start SQL Server with Docker** (example, adjust it to your setup):

```bash
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=<YourStrongPassword>" \
  -p 1433:1433 --name sqlserver -d mcr.microsoft.com/mssql/server:2022-latest
```

**5. Set up environment variables** by creating a `.env` file in the project root:

```env
SECRET_KEY=a_long_random_secret_key
# Add your database connection variables here
# (user, password, server, database name)
```

## ▶️ Running

```bash
uvicorn main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 🧭 Project status and next steps

Portfolio and learning project, not audited by third parties.

- [ ] Migrate from `python-jose` to `PyJWT` (actively maintained library)
- [ ] Add a `docker-compose.yml` to start the API and the database with a single command
- [ ] Add automated tests
- [ ] Add a `.env.example` file
- [ ] Add screenshots of `/docs`
