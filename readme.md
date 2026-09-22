# 🛡️ SecureAuth Backend

SecureAuth es una API backend desarrollada bajo una arquitectura limpia (Clean Architecture / Domain-Driven Design), construida con **FastAPI**, **SQLAlchemy** y **SQL Server**, utilizando contenedores Docker. El proyecto implementa rigurosas prácticas de seguridad, incluyendo hashing de contraseñas con bcrypt y validación estricta de datos de entrada.

---

## 🚀 Características Principales

- **Arquitectura por Capas:** Separación modular entre Dominio (`domain/`), Infraestructura (`infrastructure/`) y Esquemas de Validación (`schema/`).
- **Seguridad Robusta:** Cifrado de contraseñas mediante `passlib` y el algoritmo `bcrypt`.
- **Validación de Datos:** Uso de **Pydantic** para garantizar tipos de datos estrictos y validación automática de correos electrónicos (`EmailStr`).
- **Persistencia Empresarial:** Conexión nativa con **SQL Server** corriendo en un contenedor Docker a través de `pyodbc` y SQLAlchemy.
- **Documentación Interactiva:** Endpoints documentados automáticamente mediante Swagger UI y ReDoc (gracias a FastAPI).

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.11+**
- **FastAPI** (Framework web asíncrono de alto rendimiento)
- **SQLAlchemy** (ORM para mapeo objeto-relacional)
- **SQL Server & Docker** (Base de datos relacional en contenedores)
- **Pydantic** (Validación de datos y esquemas)
- **Passlib & Bcrypt** (Seguridad y hashing de credenciales)

---

## 📂 Estructura del Proyecto

```text
SecureAuth/
│
├── domain/               # Entidades y lógica de negocio
│   └── __init__.py
│
├── infrastructure/       # Capa de datos y seguridad
│   ├── __init__.py
│   ├── database.py       # Configuración del motor y sesión SQLAlchemy
│   ├── models.py         # Modelos de base de datos (SQL Server)
│   └── security.py       # Funciones de hashing y verificación de contraseñas
│
├── schema/               # Modelos Pydantic para validación de entrada/salida
│   └── usuario_schema.py
│
├── .env                  # Variables de entorno y credenciales (Oculto)
├── main.py               # Punto de entrada de la API (FastAPI)
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Documentación del proyecto

⚙️ Guía de Instalación y Ejecución Local
Sigue estos pasos para clonar y levantar el proyecto en tu máquina:

1. Clonar el repositorio
Bash
git clone [https://github.com/tu-usuario/SecureAuth.git](https://github.com/tu-usuario/SecureAuth.git)
cd SecureAuth
2. Crear y activar el entorno virtual
Bash
python -m venv venv

# En macOS / Linux:
source venv/bin/activate

# En Windows:
# venv\Scripts\activate
3. Instalar las dependencias
Bash
pip install -r requirements.txt
4. Configurar las variables de entorno
Crea un archivo llamado .env en la raíz del proyecto y define la cadena de conexión para tu instancia de SQL Server:

Fragmento de código
DATABASE_URL=mssql+pyodbc://sa:TuPasswordSeguro123@localhost:1433/SecureAuthDB?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes
▶️ Ejecución del Servidor
Inicia la aplicación en modo de desarrollo con Uvicorn:

Bash
uvicorn main:app --reload
La API estará corriendo en: http://127.0.0.1:8000

Documentación interactiva (Swagger UI): http://127.0.0.1:8000/docs