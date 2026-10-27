# Definiendo imagen base y directorio
FROM python:3.12.1-slim

WORKDIR /app

# Copiando dependencias e instalando
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiando código y exponiendo puerto
COPY ./app ./app
EXPOSE 8000

# Comando de ejecución de Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]