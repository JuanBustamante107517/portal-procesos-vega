# 1. Usar una imagen base de Python oficial
FROM python:3.10-slim

# 2. Evitar que Python genere archivos .pyc y permitir logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Crear carpeta de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalar dependencias del sistema necesarias para Postgres/Django
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiar el archivo de requisitos e instalarlos
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 6. Copiar todo el código del proyecto
COPY . /app/

# 7. Exponer el puerto donde corre Django
EXPOSE 8000

# 8. Comando para iniciar el servidor (usamos 0.0.0.0 para que se vea desde fuera)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]