import os
from datetime import timedelta

class Config:
    """Configuración base de la aplicación"""
    
    # Configuración de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    
    # Configuración de la aplicación
    APP_NAME = 'Teteu Cueros'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Configuración de personalizaciones
    MAX_PERSONALIZACIONES = 1000
    PERSONALIZACION_EXPIRY = timedelta(days=30)  # Las personalizaciones expiran en 30 días
    
    # Opciones de personalización
    COLORES_DISPONIBLES = ['negro', 'marron', 'marron claro']
    HERRAJES_DISPONIBLES = ['plata', 'dorado']
    
    # Configuración de archivos estáticos
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo para archivos
    
    # Configuración de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    @staticmethod
    def init_app(app):
        """Inicializar configuración específica de la aplicación"""
        pass

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    def __init__(self):
        super().__init__()
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY debe estar definida en producción")

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
