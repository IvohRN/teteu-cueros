# Guía de Despliegue - Teteu Cueros

## 🚀 Opciones de Despliegue

### **Opción 1: VPS/Cloud (Recomendado)**

#### **Requisitos del Servidor:**
- Ubuntu 20.04+ o CentOS 7+
- Python 3.8+
- Nginx
- 1GB RAM mínimo
- 10GB almacenamiento

#### **Pasos de Instalación:**

1. **Preparar servidor:**
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install python3-pip python3-venv nginx -y

# Crear usuario para la aplicación
sudo useradd -m -s /bin/bash tetey
sudo usermod -aG sudo tetey
```

2. **Configurar aplicación:**
```bash
# Cambiar a usuario tetey
sudo su - tetey

# Clonar/copiar aplicación
git clone <tu-repositorio> tetey-cueros
cd tetey-cueros

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements-prod.txt
```

3. **Configurar variables de entorno:**
```bash
# Crear archivo .env
cat > .env << EOF
SECRET_KEY=tu-clave-secreta-muy-segura
FLASK_ENV=production
FLASK_DEBUG=False
HOST=127.0.0.1
PORT=5000
LOG_LEVEL=INFO
EOF
```

4. **Configurar Nginx:**
```bash
sudo nano /etc/nginx/sites-available/tetey-cueros
```

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/tetey/tetey-cueros/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

5. **Activar sitio:**
```bash
sudo ln -s /etc/nginx/sites-available/tetey-cueros /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

6. **Configurar servicio systemd:**
```bash
sudo nano /etc/systemd/system/tetey-cueros.service
```

```ini
[Unit]
Description=Tetey Cueros Web Application
After=network.target

[Service]
User=tetey
Group=tetey
WorkingDirectory=/home/tetey/tetey-cueros
Environment=PATH=/home/tetey/tetey-cueros/venv/bin
ExecStart=/home/tetey/tetey-cueros/venv/bin/gunicorn --config gunicorn.conf.py wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

7. **Iniciar servicio:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable tetey-cueros
sudo systemctl start tetey-cueros
sudo systemctl status tetey-cueros
```

### **Opción 2: Heroku (Fácil)**

1. **Instalar Heroku CLI**
2. **Crear Procfile:**
```
web: gunicorn --config gunicorn.conf.py wsgi:app
```

3. **Desplegar:**
```bash
heroku create tetey-cueros
git push heroku main
heroku config:set SECRET_KEY=tu-clave-secreta
```

### **Opción 3: Docker (Avanzado)**

1. **Crear Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements-prod.txt .
RUN pip install -r requirements-prod.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--config", "gunicorn.conf.py", "wsgi:app"]
```

2. **Crear docker-compose.yml:**
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=tu-clave-secreta
      - FLASK_ENV=production
    volumes:
      - ./static:/app/static
```

## 🔒 Configuración de Seguridad

### **Variables de Entorno Importantes:**
```bash
SECRET_KEY=clave-muy-segura-de-al-menos-32-caracteres
FLASK_ENV=production
FLASK_DEBUG=False
```

### **Headers de Seguridad:**
- Configurar HTTPS
- Headers de seguridad (HSTS, CSP)
- Rate limiting
- Firewall configurado

## 📊 Monitoreo

### **Logs:**
```bash
# Ver logs de la aplicación
sudo journalctl -u tetey-cueros -f

# Ver logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### **Estadísticas:**
- Acceder a `/admin/personalizaciones` para ver estadísticas
- Monitorear uso de CPU y memoria
- Configurar alertas

## 🔄 Actualizaciones

### **Proceso de actualización:**
```bash
# Detener servicio
sudo systemctl stop tetey-cueros

# Actualizar código
git pull origin main

# Instalar nuevas dependencias
source venv/bin/activate
pip install -r requirements-prod.txt

# Reiniciar servicio
sudo systemctl start tetey-cueros
```

## 🆘 Solución de Problemas

### **Problemas Comunes:**

1. **Error 502 Bad Gateway:**
   - Verificar que Gunicorn esté ejecutándose
   - Revisar logs: `sudo journalctl -u tetey-cueros`

2. **Archivos estáticos no cargan:**
   - Verificar permisos de archivos
   - Revisar configuración de Nginx

3. **Base de datos no funciona:**
   - Verificar permisos de archivo de BD
   - Revisar logs de aplicación

### **Comandos de Diagnóstico:**
```bash
# Estado del servicio
sudo systemctl status tetey-cueros

# Verificar puertos
sudo netstat -tlnp | grep :5000

# Verificar logs
sudo journalctl -u tetey-cueros --since "1 hour ago"
```
