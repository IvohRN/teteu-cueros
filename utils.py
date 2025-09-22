"""
Utilidades para la aplicación Teteu Cueros
"""

import os
import logging
from typing import Dict, Any, Optional
from flask import request, flash, redirect, url_for, render_template

def setup_logging():
    """Configurar logging para la aplicación"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def validar_datos_personalizacion(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validar datos de personalización
    
    Args:
        data: Diccionario con los datos a validar
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    from config import Config
    
    # Verificar campos requeridos
    campos_requeridos = ['color', 'herrajes']
    for campo in campos_requeridos:
        if not data.get(campo):
            return False, f"El campo {campo} es requerido"
    
    # Validar color
    color = data.get('color')
    if color not in Config.COLORES_DISPONIBLES:
        return False, f"Color '{color}' no es válido. Colores disponibles: {', '.join(Config.COLORES_DISPONIBLES)}"
    
    # Validar herrajes
    herrajes = data.get('herrajes')
    if herrajes not in Config.HERRAJES_DISPONIBLES:
        return False, f"Herrajes '{herrajes}' no son válidos. Herrajes disponibles: {', '.join(Config.HERRAJES_DISPONIBLES)}"
    
    return True, None

def obtener_datos_formulario() -> Dict[str, Any]:
    """Obtener y limpiar datos del formulario"""
    return {
        'color': request.form.get('color', '').strip(),
        'herrajes': request.form.get('herrajes', '').strip(),
        'modelo': request.args.get('modelo', 'Cartera')
    }

def manejar_error(error: Exception, mensaje_usuario: str = "Ocurrió un error inesperado") -> str:
    """
    Manejar errores de la aplicación
    
    Args:
        error: Excepción capturada
        mensaje_usuario: Mensaje amigable para el usuario
        
    Returns:
        str: Mensaje de error para mostrar al usuario
    """
    logger = logging.getLogger(__name__)
    logger.error(f"Error en la aplicación: {str(error)}", exc_info=True)
    
    return mensaje_usuario

def verificar_archivo_imagen(ruta_imagen: str) -> bool:
    """
    Verificar si existe un archivo de imagen
    
    Args:
        ruta_imagen: Ruta del archivo de imagen
        
    Returns:
        bool: True si el archivo existe, False en caso contrario
    """
    if not ruta_imagen:
        return False
    
    # Remover el prefijo /static/ para obtener la ruta real
    ruta_real = ruta_imagen.replace('/static/', 'static/')
    return os.path.exists(ruta_real)

def obtener_imagen_por_defecto(modelo: str) -> str:
    """
    Obtener imagen por defecto para un modelo
    
    Args:
        modelo: Nombre del modelo
        
    Returns:
        str: Ruta de la imagen por defecto
    """
    if 'urbana' in modelo.lower():
        return '/static/modelo2.jpg'
    return '/static/modelo1.jpg'

def sanitizar_input(texto: str) -> str:
    """
    Sanitizar entrada de usuario para prevenir XSS
    
    Args:
        texto: Texto a sanitizar
        
    Returns:
        str: Texto sanitizado
    """
    if not texto:
        return ""
    
    # Remover caracteres peligrosos
    caracteres_peligrosos = ['<', '>', '"', "'", '&']
    for char in caracteres_peligrosos:
        texto = texto.replace(char, '')
    
    return texto.strip()

def formatear_precio(precio: float) -> str:
    """
    Formatear precio para mostrar
    
    Args:
        precio: Precio numérico
        
    Returns:
        str: Precio formateado
    """
    return f"${precio:,.2f}"

def obtener_info_navegador() -> Dict[str, str]:
    """
    Obtener información del navegador del usuario
    
    Returns:
        Dict: Información del navegador
    """
    user_agent = request.headers.get('User-Agent', '')
    
    # Detectar navegador
    if 'Chrome' in user_agent:
        navegador = 'Chrome'
    elif 'Firefox' in user_agent:
        navegador = 'Firefox'
    elif 'Safari' in user_agent:
        navegador = 'Safari'
    elif 'Edge' in user_agent:
        navegador = 'Edge'
    else:
        navegador = 'Otro'
    
    # Detectar sistema operativo
    if 'Windows' in user_agent:
        so = 'Windows'
    elif 'Mac' in user_agent:
        so = 'macOS'
    elif 'Linux' in user_agent:
        so = 'Linux'
    else:
        so = 'Otro'
    
    return {
        'navegador': navegador,
        'sistema_operativo': so,
        'user_agent': user_agent
    }
