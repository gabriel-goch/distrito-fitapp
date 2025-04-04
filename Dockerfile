FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Variable de entorno para puerto
ENV PORT=5000

# Puerto que escuchará la aplicación
EXPOSE 5000

# Comando para iniciar la aplicación
CMD gunicorn --bind 0.0.0.0:$PORT main:app
