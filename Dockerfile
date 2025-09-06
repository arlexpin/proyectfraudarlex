# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos y lo instala
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia la configuración de Streamlit primero
COPY .streamlit/ .streamlit/

# Copia el resto de la aplicación
COPY . .

# Crear directorio para archivos estáticos de Streamlit
RUN mkdir -p /app/.streamlit/static

# Expone el puerto en el que se ejecuta Streamlit
EXPOSE 8501

# Configurar variables de entorno para Streamlit
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Comando para ejecutar la aplicación con configuración optimizada
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501", "--server.headless", "true"]
