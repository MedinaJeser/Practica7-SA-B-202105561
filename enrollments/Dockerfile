# Usar Python en su versión ligera (Alpine)
FROM python:3.11-alpine

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apk add --no-cache gcc musl-dev libffi-dev

# Copiar los archivos de dependencias
COPY requirements.txt .

# Instalar dependencias con pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto en el que correrá la aplicación
EXPOSE 8002

# Comando de inicio del servicio FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]