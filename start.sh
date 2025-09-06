#!/bin/bash
# Script de inicio optimizado específicamente para Render
# Este script resuelve problemas de carga de módulos JavaScript dinámicos

# Configurar variables de entorno críticas para Render
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
export STREAMLIT_SERVER_MAX_MESSAGE_SIZE=200
export STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION=false
export STREAMLIT_SERVER_RUN_ON_SAVE=false
export STREAMLIT_SERVER_ALLOW_RUN_ON_SAVE=false
export STREAMLIT_CLIENT_TOOLBAR_MODE=minimal
export STREAMLIT_CLIENT_SHOW_SIDEBAR_NAVIGATION=false
export STREAMLIT_GLOBAL_DEVELOPMENT_MODE=false
export STREAMLIT_GLOBAL_SHOW_WARNING_ON_DIRECT_EXECUTION=false

# Configuración específica para evitar problemas de CDN
export STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
export STREAMLIT_SERVER_PORT=${PORT:-8501}
export STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Crear directorio de configuración si no existe
mkdir -p .streamlit

# Copiar configuración específica para Render
cp .streamlit/config.render.toml .streamlit/config.toml

# Ejecutar Streamlit con configuración específica para Render
exec streamlit run app.py \
  --server.address 0.0.0.0 \
  --server.port ${PORT:-8501} \
  --server.headless true \
  --server.enableCORS false \
  --server.enableXsrfProtection false \
  --browser.gatherUsageStats false \
  --server.maxUploadSize 200 \
  --server.maxMessageSize 200 \
  --server.enableWebsocketCompression false \
  --server.runOnSave false \
  --server.allowRunOnSave false \
  --client.toolbarMode minimal \
  --client.showSidebarNavigation false \
  --global.developmentMode false \
  --global.showWarningOnDirectExecution false \
  --server.fileWatcherType none
