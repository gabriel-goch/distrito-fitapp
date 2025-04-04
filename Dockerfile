RUN echo "#!/bin/bash\necho 'Iniciando aplicación...'\necho 'Variables: PORT=${PORT}'\nls -la\ngunicorn --bind 0.0.0.0:${PORT} --timeout 120 main:app" > /app/start.sh
    chmod +x /app/start.sh

# Ejecutar con script para asegurar las variables de entorno
CMD ["/app/start.sh"]
