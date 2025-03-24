# Usamos Python 3.10 como base
FROM python:3.10

# Definir directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . .

# Comando por defecto para iniciar Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
