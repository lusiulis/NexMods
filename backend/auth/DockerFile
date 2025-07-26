# Etapa base
FROM python:3.11-slim

# Variables de entorno para UTF-8 y no generar archivos pyc
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=UTC

# Seteamos el directorio de trabajo
WORKDIR /app

# Instalamos dependencias del sistema
RUN apt-get update && apt-get install -y build-essential && apt-get clean

# Copiamos los requirements e instalamos dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de la aplicación
COPY ./app ./app

# Comando por defecto para desarrollo (con autoreload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
