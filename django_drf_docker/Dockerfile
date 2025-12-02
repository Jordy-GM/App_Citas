# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia el archivo de requisitos
COPY requirements.txt /app/

# Instala las dependencias de Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copia todo el proyecto
COPY . /app/

# Expone el puerto 8000
EXPOSE 8000

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]