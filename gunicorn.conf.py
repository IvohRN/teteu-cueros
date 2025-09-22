# Configuración de Gunicorn para producción

# Configuración del servidor
bind = "0.0.0.0:10000"
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Configuración de logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Configuración de seguridad
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configuración de procesos
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# Configuración de archivos estáticos
static_map = {
    '/static': 'static'
}
