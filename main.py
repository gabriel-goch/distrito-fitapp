import os
from flask import Flask

# Crear la aplicación directamente
app = Flask(__name__)

# Configuración básica
app.config.update(
    SECRET_KEY=os.environ.get('SESSION_SECRET', 'dev-key-for-testing'),
)

# Endpoint simple de health check
@app.route('/')
@app.route('/health')
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    # Para desarrollo y producción
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
