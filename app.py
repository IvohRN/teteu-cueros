"""
Aplicación principal de Teteu Cueros
Sistema de personalización de carteras de cuero
"""

from flask import Flask, render_template, request, redirect, url_for, flash, abort
import logging
from config import config
from models import PersonalizacionManager
from utils import (
    setup_logging, 
    validar_datos_personalizacion, 
    obtener_datos_formulario,
    manejar_error,
    verificar_archivo_imagen,
    obtener_imagen_por_defecto,
    sanitizar_input
)

def create_app(config_name='default'):
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Configurar logging
    logger = setup_logging()
    
    # Inicializar gestor de personalizaciones
    personalizaciones_manager = PersonalizacionManager()
    
    # Rutas de la aplicación
    @app.route('/', methods=['GET'])
    def pagina_principal():
        """Página principal con catálogo de carteras"""
        try:
            return render_template('index.html')
        except Exception as e:
            logger.error(f"Error en página principal: {str(e)}")
            return render_template('error.html', 
                                 error_code=500, 
                                 error_message="Error interno del servidor")
    
    @app.route('/personalizar_form', methods=['GET'])
    def formulario():
        """Formulario de personalización"""
        try:
            modelo = sanitizar_input(request.args.get('modelo', 'Cartera'))
            
            # Determinar imagen según modelo
            imagen = obtener_imagen_por_defecto(modelo)
            
            return render_template('personalizar.html', 
                                modelo=modelo, 
                                imagen=imagen)
        except Exception as e:
            logger.error(f"Error en formulario: {str(e)}")
            return render_template('error.html', 
                                 error_code=500, 
                                 error_message="Error al cargar el formulario")
    
    @app.route('/personalizar', methods=['POST'])
    def personalizar():
        """Procesar personalización y generar enlace"""
        try:
            # Obtener datos del formulario
            datos = obtener_datos_formulario()
            
            # Validar datos
            es_valido, mensaje_error = validar_datos_personalizacion(datos)
            if not es_valido:
                flash(mensaje_error, 'error')
                return redirect(url_for('formulario', modelo=datos['modelo']))
            
            # Crear personalización
            personalizacion = personalizaciones_manager.crear_personalizacion(
                producto=datos['modelo'],
                color=datos['color'],
                herrajes=datos['herrajes']
            )
            
            # Generar enlace
            enlace = url_for('ver_personalizacion', id=personalizacion.id, _external=True)
            
            logger.info(f"Personalización creada: {personalizacion.id}")
            return enlace
            
        except ValueError as e:
            logger.warning(f"Error de validación: {str(e)}")
            flash(str(e), 'error')
            return redirect(url_for('formulario', modelo=request.args.get('modelo', 'Cartera')))
        except Exception as e:
            logger.error(f"Error al procesar personalización: {str(e)}")
            return render_template('error.html', 
                                 error_code=500, 
                                 error_message="Error al procesar la personalización")
    
    @app.route('/ver/<id>')
    def ver_personalizacion(id):
        """Mostrar personalización específica"""
        try:
            # Obtener personalización
            personalizacion = personalizaciones_manager.obtener_personalizacion(id)
            
            if not personalizacion:
                logger.warning(f"Personalización no encontrada: {id}")
                return render_template('error.html', 
                                     error_code=404, 
                                     error_message="Personalización no encontrada")
            
            # Obtener ruta de imagen
            img_path = personalizacion.get_imagen_path()
            
            # Verificar si la imagen existe
            if not verificar_archivo_imagen(img_path):
                img_path = obtener_imagen_por_defecto(personalizacion.producto)
            
            return render_template('ver_personalizacion.html', 
                                personalizacion=personalizacion, 
                                img_path=img_path)
            
        except Exception as e:
            logger.error(f"Error al mostrar personalización {id}: {str(e)}")
            return render_template('error.html', 
                                 error_code=500, 
                                 error_message="Error al cargar la personalización")
    
    @app.route('/admin/personalizaciones')
    def admin_personalizaciones():
        """Panel de administración (solo para desarrollo)"""
        if not app.config['DEBUG']:
            abort(404)
        
        try:
            personalizaciones = personalizaciones_manager.listar_personalizaciones()
            return render_template('admin.html', personalizaciones=personalizaciones)
        except Exception as e:
            logger.error(f"Error en panel de administración: {str(e)}")
            return render_template('error.html', 
                                 error_code=500, 
                                 error_message="Error en panel de administración")
    
    @app.route('/admin/limpiar')
    def admin_limpiar():
        """Limpiar personalizaciones expiradas"""
        if not app.config['DEBUG']:
            abort(404)
        
        try:
            eliminadas = personalizaciones_manager.limpiar_personalizaciones_expiradas()
            flash(f"Se eliminaron {eliminadas} personalizaciones expiradas", 'success')
            return redirect(url_for('admin_personalizaciones'))
        except Exception as e:
            logger.error(f"Error al limpiar personalizaciones: {str(e)}")
            flash("Error al limpiar personalizaciones", 'error')
            return redirect(url_for('admin_personalizaciones'))
    
    # Manejo de errores
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('error.html', 
                             error_code=404, 
                             error_message="Página no encontrada")
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Error interno: {str(error)}")
        return render_template('error.html', 
                             error_code=500, 
                             error_message="Error interno del servidor")
    
    # Context processors
    @app.context_processor
    def inject_config():
        """Inyectar configuración en templates"""
        return {
            'app_name': app.config['APP_NAME'],
            'debug': app.config['DEBUG']
        }
    
    return app

# Crear aplicación
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
