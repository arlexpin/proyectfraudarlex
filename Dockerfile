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

# Copia toda la aplicación de una vez
COPY . .

# Hacer el script de inicio ejecutable
RUN chmod +x start.sh

# Expone el puerto en el que se ejecuta Streamlit
EXPOSE 8501

# Configurar variables de entorno específicas para Render
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
ENV STREAMLIT_SERVER_MAX_MESSAGE_SIZE=200
ENV STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION=false
ENV STREAMLIT_SERVER_RUN_ON_SAVE=false
ENV STREAMLIT_SERVER_ALLOW_RUN_ON_SAVE=false
ENV STREAMLIT_CLIENT_TOOLBAR_MODE=minimal
ENV STREAMLIT_CLIENT_SHOW_SIDEBAR_NAVIGATION=false
ENV STREAMLIT_GLOBAL_DEVELOPMENT_MODE=false
ENV STREAMLIT_GLOBAL_SHOW_WARNING_ON_DIRECT_EXECUTION=false
ENV STREAMLIT_SERVER_FILE_WATCHER_TYPE=none

# Usar el script de inicio personalizado
CMD ["./start.sh"]