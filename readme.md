🛡️ SecureAuth Backend
(Versión en Español / Spanish Version)

SecureAuth es una API backend de grado empresarial desarrollada bajo un enfoque de arquitectura limpia y Domain-Driven Design (DDD). Construida con FastAPI, SQLAlchemy y SQL Server (en contenedores Docker), está diseñada para ofrecer altos estándares de seguridad, trazabilidad forense y control de acceso robusto en entornos B2B.

🚀 Características Principales y Seguridad Enterprise
Autenticación Basada en Cookies Seguras: Empleo de cookies HttpOnly, Secure y SameSite=lax para mitigar ataques XSS.

Gestión de Sesión Única (jti): Control estricto de tokens mediante identificadores únicos validados en base de datos.

Control de Acceso Basado en Roles (RBAC): Endpoints administrativos protegidos (/admin/*) con validación de privilegios.

Protección Anti-Fuerza Bruta: Limitación de tasa de peticiones (slowapi) en rutas críticas de autenticación (5 req/min).

Auditoría Forense: Registro automático en base de datos (AuditLogModel) capturando acciones y la IP de origen del cliente.

Manejo Global de Excepciones: Controladores centralizados para errores de base de datos (pyodbc) y del servidor.

🛡️ SecureAuth Backend
(English Version)

SecureAuth is an enterprise-grade backend API built under a Clean Architecture and Domain-Driven Design (DDD) approach. Powered by FastAPI, SQLAlchemy, and SQL Server (via Docker containers), it is engineered to deliver high security standards, forensic traceability, and robust access control for B2B environments.

🚀 Key Features & Enterprise Security
Secure Cookie-Based Authentication: Utilization of HttpOnly, Secure, and SameSite=lax cookies to mitigate XSS attacks.

Single-Session Management (jti): Strict token control via unique session identifiers validated against the database.

Role-Based Access Control (RBAC): Protected administrative endpoints (/admin/*) with strict privilege validation.

Brute-Force Protection: Rate limiting (slowapi) integrated into critical authentication routes (5 req/min).

Forensic Auditing: Automated database logging (AuditLogModel) capturing critical user actions and client IP addresses.

Global Exception Handling: Centralized handlers for database connection drops (pyodbc) and internal server errors.

🛠️ Stack Tecnológico / Technology Stack
Python 3.11+

FastAPI (High-performance async web framework)

SQLAlchemy & pyodbc (ORM and native connector for MS SQL Server with READ COMMITTED isolation)

Docker & SQL Server (Persistent relational database infrastructure)

Pydantic & Passlib (Bcrypt) (Schema validation and secure credential hashing)

SlowAPI & Python-Jose (Rate limiting and encrypted JWT management)

📂 Estructura del Proyecto / Project Structure
Plaintext
SecureAuth/
│
├── domain/               # Entidades de dominio y lógica de negocio orientada a objetos
├── infrastructure/       # Capa de datos, persistencia, modelos y seguridad (JWT, JTI, Auditoría)
├── schema/               # Esquemas Pydantic para validación y tipado de entrada/salida
├── .env                  # Variables de entorno y secretos del sistema (Oculto)
├── main.py               # Enrutamiento principal, middleware de seguridad y manejo de errores
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Documentación del proyecto
⚙️ Guía de Instalación / Installation Guide
Bash
# 1. Clonar el repositorio / Clone repository
git clone https://github.com/tu-usuario/SecureAuth.git
cd SecureAuth

# 2. Crear y activar entorno virtual / Create & activate virtual environment
python -m venv venv
# Linux/macOS: source venv/bin/activate
# Windows: venv\Scripts\activate

# 3. Instalar dependencias / Install dependencies
pip install -r requirements.txt

# 4. Configurar variables de entorno (.env) / Set up environment variables
SECRET_KEY=tu_clave_secreta_extremadamente_larga_y_segura
▶️ Ejecución / Execution
Bash
uvicorn main:app --reload
API Endpoint: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)