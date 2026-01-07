# MacroTrack API 🥗

Backend escalable desarrollado con **FastAPI** y **Python** para la aplicación MacroTrack.

## 🚀 Características

- **Arquitectura Limpia**: Separación clara de responsabilidades (api, models, schemas, services).
- **Configuración por Entorno**: Uso de `.env` para variables sensibles y configuración.
- **Validación Robusta**: Pydantic para validación de datos de entrada y salida.
- **Base de Datos Ready**: Configurado con SQLAlchemy (SQLite por defecto para desarrollo).
- **Cálculos Nutricionales**: Endpoints implementados con las fórmulas Mifflin-St Jeor y TDEE.

## 🛠️ Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)

## 📦 Instalación y Uso

1. **Entorno Virtual**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instalar Dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar el Servidor**:

   ```bash
   uvicorn app.main:app --reload
   ```

4. **Documentación Interactiva**:
   Accede a [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para ver la documentación de Swagger.

## 📁 Estructura del Proyecto

```
app/
├── api/             # Versiones de la API y endpoints
├── core/            # Configuración, seguridad y constantes
├── db/              # Sesión de BD y clases base
├── models/          # Modelos de SQLAlchemy
├── schemas/         # Esquemas de Pydantic
├── services/        # Lógica de negocio secundaria
└── main.py          # Punto de entrada de la aplicación
```

## 📊 Endpoints Implementados

- `POST /api/v1/calculator/calculate-macros`: Calcula BMR, TDEE y distribución de macros según los datos del usuario.
