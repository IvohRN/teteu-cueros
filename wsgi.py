"""
Archivo WSGI para despliegue en producción
"""

import os
from app import create_app

# Crear aplicación con configuración de producción
app = create_app('production')

if __name__ == "__main__":
    app.run()
