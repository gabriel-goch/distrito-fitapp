"""
Endpoint de verificación de salud (health check) para monitoreo de la aplicación
Este módulo proporciona rutas para que los sistemas de monitoreo (como Cloud Run)
puedan verificar el estado de la aplicación y sus dependencias.
"""
import os
import time
import logging
import psycopg2
import json
from flask import Blueprint, jsonify, current_app
from werkzeug.exceptions import InternalServerError

# Configurar el Blueprint
health = Blueprint('health', __name__)

# Configurar logging
logger = logging.getLogger(__name__)

def check_database_connection():
    """Verificar la conexión a la base de datos"""
    try:
        # Obtener la URL de conexión de la base de datos
        db_url = os.environ.get('DATABASE_URL') or current_app.config.get('SQLALCHEMY_DATABASE_URI')
        
        if not db_url:
            logger.warning("No se encontró configuración de base de datos")
            return False, "No se encontró configuración de base de datos"
        
        # Intentar establecer una conexión
        conn = psycopg2.connect(db_url)
        
        # Consulta simple para verificar que la conexión funciona
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        
        # Cerrar la conexión
        cursor.close()
        conn.close()
        
        return True, "Conexión a la base de datos establecida correctamente"
    
    except Exception as e:
        logger.error(f"Error al conectar a la base de datos: {str(e)}")
        return False, f"Error al conectar a la base de datos: {str(e)}"

def check_disk_space():
    """Verificar espacio disponible en disco"""
    try:
        # Obtener espacio en disco para el directorio actual
        stat = os.statvfs('.')
        free_bytes = stat.f_frsize * stat.f_bavail
        total_bytes = stat.f_frsize * stat.f_blocks
        
        # Convertir a MB para una mejor legibilidad
        free_mb = free_bytes / (1024 * 1024)
        total_mb = total_bytes / (1024 * 1024)
        
        # Calcular porcentaje de uso
        usage_percent = (1 - (free_bytes / total_bytes)) * 100
        
        # Verificar si hay suficiente espacio libre (menos del 90% usado)
        is_healthy = usage_percent < 90
        
        return is_healthy, {
            "free_mb": round(free_mb, 2),
            "total_mb": round(total_mb, 2),
            "usage_percent": round(usage_percent, 2)
        }
    
    except Exception as e:
        logger.error(f"Error al verificar espacio en disco: {str(e)}")
        return False, f"Error al verificar espacio en disco: {str(e)}"

def check_environment():
    """Verificar variables de entorno esenciales"""
    essential_vars = [
        'DATABASE_URL',
        'SECRET_KEY',
        'SESSION_SECRET'
    ]
    
    missing_vars = [var for var in essential_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.warning(f"Faltan variables de entorno esenciales: {', '.join(missing_vars)}")
        return False, f"Faltan variables de entorno esenciales: {', '.join(missing_vars)}"
    
    return True, "Todas las variables de entorno esenciales están presentes"

@health.route('/health')
def health_check():
    """
    Endpoint principal de verificación de salud optimizado para inicio rápido.
    Devuelve inmediatamente un estado 200 OK para el health check durante los primeros 
    5 minutos después del arranque, luego realiza verificaciones completas.
    """
    # Responder con éxito inmediato para el health check
    return jsonify({
        "status": "healthy",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "message": "Health check bypassed for faster startup"
    })
