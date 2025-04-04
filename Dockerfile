FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt primero para aprovechar el caché de capas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto (definido por la variable de entorno PORT)
ENV PORT=5000
EXPOSE ${PORT}

# Script de inicio simplificado
RUN echo '#!/bin/bash\ngunicorn --bind 0.0.0.0:${PORT} --timeout 120 main:app' > /app/start.sh && \
    chmod +x /app/start.sh

# Ejecutar con script para asegurar las variables de entorno
CMD ["/app/start.sh"]
