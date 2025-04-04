import os
from app import app
from flask import send_from_directory, render_template, redirect

# Importar los modelos esenciales primero
import models  # Modelo base

# Ruta para servir el archivo HTML estático en la raíz
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Ruta de diagnóstico directa a nivel raíz
@app.route('/superadmin-diagnostico')
def superadmin_diagnostico():
    return send_from_directory('static', 'superadmin_diagnostico.html')

# Importar los blueprints esenciales
from routes.health import health

# Registrar los blueprints que no están en app.py
app.register_blueprint(health)

# Endpoint de health check directo para optimizar respuesta
@app.route('/health')
def direct_health_check():
    """Health check optimizado para Google Cloud Run.
    Este endpoint responde inmediatamente para mejorar los tiempos de verificación.
    """
    return {"status": "healthy", "service": "distrito-fitapp"}, 200

# Manejar requests de health check para Google Cloud Run (compatible con versiones antiguas)
@app.route('/_ah/health')
def legacy_health_check():
    """Health check para Google Cloud Run (ruta legacy)."""
    return redirect('/health')

# Cargar el resto de los modelos después de los endpoints críticos
import models_subscription  # Modelo de suscripciones
import models_affiliate  # Nuevo modelo de afiliados
import models_social_auth  # Modelo de autenticación social

if __name__ == "__main__":
    # Para desarrollo local
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
else:
    # Para producción (Google Cloud Run)
    # El puerto vendrá como variable de entorno PORT
    port = int(os.environ.get("PORT", 8080))
    # En producción, el modo debug debe estar desactivado
    app.debug = False
