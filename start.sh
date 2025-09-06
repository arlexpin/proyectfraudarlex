#!/bin/bash
# Script de inicio optimizado para Render
# Este script configura el entorno y ejecuta Streamlit con las mejores prácticas

# Configurar variables de entorno para Render
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
export STREAMLIT_SERVER_PORT=${PORT:-8501}
export STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Crear directorio de configuración si no existe
mkdir -p .streamlit

# Ejecutar Streamlit con configuración optimizada
streamlit run app.py \
  --server.address 0.0.0.0 \
  --server.port ${PORT:-8501} \
  --server.headless true \
  --server.enableCORS false \
  --server.enableXsrfProtection false \
  --browser.gatherUsageStats false
