# Teteu Cueros - Sistema de Personalización de Carteras

Sistema web para personalización de carteras de cuero con Flask.

## 🚀 Características

- **Personalización visual** de carteras en tiempo real
- **Múltiples modelos** de carteras disponibles
- **Sistema de enlaces únicos** para compartir personalizaciones
- **Interfaz responsiva** y moderna
- **Validación de datos** y manejo de errores
- **Panel de administración** para desarrollo

## 📁 Estructura del Proyecto

```
mi_app/
├── app.py                 # Aplicación principal Flask
├── models.py              # Modelos de datos
├── utils.py               # Utilidades y funciones auxiliares
├── config.py              # Configuración de la aplicación
├── requirements.txt       # Dependencias Python
├── templates/             # Plantillas HTML
│   ├── base.html         # Plantilla base
│   ├── index.html        # Página principal
│   ├── personalizar.html  # Formulario de personalización
│   ├── ver_personalizacion.html # Vista de personalización
│   ├── error.html        # Página de errores
│   └── admin.html        # Panel de administración
├── static/               # Recursos estáticos
│   ├── css/
│   │   └── style.css     # Estilos CSS
│   ├── js/
│   │   └── main.js       # JavaScript
│   └── [imágenes...]     # Imágenes de productos
└── README.md             # Este archivo
```

## 🛠️ Instalación y Uso

### Requisitos
- Python 3.7+
- Flask 2.3.3

### Instalación
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py
```

### Acceso
- **Aplicación:** http://localhost:5000
- **Panel Admin:** http://localhost:5000/admin/personalizaciones (solo en desarrollo)

## 🎨 Modelos de Carteras

### Modelo 1: Cartera Clásica
- **Medidas:** 30cm alto x 46cm ancho x 17cm profundidad
- **Estilo:** Elegante y funcional

### Modelo 2: Cartera Urbana
- **Medidas:** 26cm ancho x 22cm alto x 10cm profundidad
- **Estilo:** Moderno y compacto

## 🎨 Opciones de Personalización

### Colores Disponibles
- Negro
- Marrón
- Marrón Claro

### Herrajes Disponibles
- Plata
- Dorado

## 🔧 Configuración

### Variables de Entorno
- `SECRET_KEY`: Clave secreta para Flask
- `FLASK_DEBUG`: Modo debug (True/False)
- `LOG_LEVEL`: Nivel de logging (INFO, DEBUG, ERROR)

### Configuración de Desarrollo
```python
# config.py
class DevelopmentConfig(Config):
    DEBUG = True
```

## 📱 Características Técnicas

### Frontend
- **HTML5** semántico
- **CSS3** con diseño responsivo
- **JavaScript** vanilla para interactividad
- **Vista previa en tiempo real** de personalizaciones

### Backend
- **Flask** como framework web
- **Arquitectura modular** con separación de responsabilidades
- **Validación de datos** robusta
- **Manejo de errores** completo
- **Logging** configurado

### Seguridad
- **Sanitización** de entradas de usuario
- **Validación** de datos del formulario
- **Prevención** de inyecciones XSS

## 🚀 Despliegue en Render

### Configuración para Render
1. **Archivo render.yaml** - Configuración automática del servicio
2. **Gunicorn** configurado para producción
3. **Variables de entorno** configuradas
4. **Puerto 10000** para compatibilidad con Render

### Pasos para desplegar:
1. Subir código a GitHub
2. Conectar repositorio en Render
3. Configurar variables de entorno
4. Desplegar automáticamente

## 🚀 Mejoras Implementadas

### Fase 1 ✅
1. **Separación de HTML/CSS/JS** en archivos independientes
2. **Validación básica** de datos de entrada
3. **Manejo de errores** mejorado con páginas de error personalizadas
4. **Configuración para despliegue** en Render

### Próximas Fases
- **Base de datos** para persistencia
- **Tests automatizados**
- **Optimización de rendimiento**
- **Integración con Tienda Nube**

## 📊 Panel de Administración

Accesible en modo desarrollo en `/admin/personalizaciones`:
- Ver todas las personalizaciones
- Limpiar personalizaciones expiradas
- Estadísticas básicas

## 🔍 Logging y Monitoreo

- **Logs estructurados** con timestamps
- **Niveles de logging** configurables
- **Manejo de errores** con contexto

## 📝 API Endpoints

- `GET /` - Página principal
- `GET /personalizar_form` - Formulario de personalización
- `POST /personalizar` - Procesar personalización
- `GET /ver/<id>` - Ver personalización específica
- `GET /admin/personalizaciones` - Panel de administración

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
