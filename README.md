# Sistema de Detección de Fraude en Tiempo Real

## 📋 Descripción
Sistema de detección de fraude que procesa transacciones en tiempo real utilizando múltiples modelos de Machine Learning. Integra FastAPI, Kafka, PostgreSQL y modelos de ML para proporcionar predicciones de fraude instantáneas.

## 🏗️ Arquitectura
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Kafka     │───▶│   FastAPI   │───▶│ PostgreSQL  │
│ (Producer)  │    │ (Consumer)  │    │ (Storage)   │
└─────────────┘    └─────────────┘    └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │   Models    │
                   │ (ML Models) │
                   └─────────────┘
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.9+
- Docker y Docker Compose
- PostgreSQL (opcional, se incluye en Docker)

### Instalación Local

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd app-3
```

2. **Crear entorno virtual**
```bash
python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
# Crear archivo .env
cp .env.example .env
# Editar .env con tus credenciales
```

5. **Ejecutar con Docker (recomendado)**
```bash
docker-compose up -d
```

### Instalación Solo Docker
```bash
docker-compose up -d
```

## 🔧 Configuración

### Variables de Entorno (.env)
```env
# Base de datos
DATABASE_URL=postgresql://fraud_user:fraud_password@localhost:5432/fraud_detection

# Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_SASL_MECHANISMS=PLAIN
KAFKA_SECURITY_PROTOCOL=PLAINTEXT
KAFKA_TOPIC_INPUT=transactions_stream
KAFKA_TOPIC_OUTPUT=fraud_predictions

# Aplicación
ENVIRONMENT=development
LOG_LEVEL=INFO
MODEL_PATH=./model
```

## 🎯 Uso

### Iniciar la Aplicación
```bash
# Desarrollo local
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Con Docker
docker-compose up -d
```

### Endpoints Disponibles

- **GET** `/health` - Estado de la aplicación
- **GET** `/start-consuming` - Iniciar consumo de transacciones
- **GET** `/transaction/{transaction_id}` - Obtener resultado de transacción

### Enviar Transacciones
```bash
# Ejemplo de transacción
curl -X POST "http://localhost:8000/transaction" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "12345",
    "amount": 100.50,
    "time": 1234567890,
    "v1": 0.1,
    "v2": 0.2,
    ...
    "v28": 0.28
  }'
```

## 🤖 Modelos de Machine Learning

El sistema utiliza 5 modelos diferentes:

1. **Regresión Logística** (`logistic_regression_model.pkl`)
2. **K-Nearest Neighbors** (`knears_neighbors_model.pkl`)
3. **Support Vector Classifier** (`svc_model.pkl`)
4. **Árbol de Decisión** (`decision_tree_model.pkl`)
5. **Red Neuronal Keras** (`undersample_model.h5`)

## 📊 Monitoreo

### Kafka UI
- URL: http://localhost:8080
- Monitoreo de tópicos y mensajes

### Logs
```bash
# Ver logs de la aplicación
docker-compose logs -f app

# Ver logs de todos los servicios
docker-compose logs -f
```

## 🧪 Testing

### Ejecutar Tests
```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
pytest tests/
```

### Tests de Integración
```bash
# Test completo del flujo
python -m pytest tests/test_integration.py -v
```

## 🚀 Despliegue

### Producción
```bash
# Construir imagen de producción
docker build -t fraud-detection:latest .

# Ejecutar en producción
docker-compose -f docker-compose.prod.yml up -d
```

### Variables de Entorno de Producción
```env
ENVIRONMENT=production
LOG_LEVEL=WARNING
DATABASE_URL=<production-db-url>
KAFKA_BOOTSTRAP_SERVERS=<production-kafka-url>
```

## 📁 Estructura del Proyecto

```
app-3/
├── main.py                 # Aplicación FastAPI principal
├── config.py              # Configuración de la aplicación
├── db.py                  # Operaciones de base de datos
├── kafka_client.py        # Cliente Kafka
├── prediction.py          # Modelos de ML y predicciones
├── requirements.txt       # Dependencias de Python
├── Dockerfile            # Configuración de Docker
├── docker-compose.yml     # Orquestación de servicios
├── model/                 # Modelos de ML entrenados
│   ├── logistic_regression_model.pkl
│   ├── knears_neighbors_model.pkl
│   ├── svc_model.pkl
│   ├── decision_tree_model.pkl
│   └── undersample_model.h5
├── tests/                 # Tests unitarios e integración
├── schemas.py             # Esquemas Pydantic
├── logging_config.py      # Configuración de logging
└── README.md             # Esta documentación
```

## 🔒 Seguridad

- Autenticación JWT (pendiente)
- Validación de entrada con Pydantic
- Rate limiting (pendiente)
- HTTPS en producción (pendiente)

## 📈 Métricas y Monitoreo

- Health checks automáticos
- Logs estructurados
- Métricas de rendimiento (pendiente)
- Alertas automáticas (pendiente)

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico, contactar:
- Email: soporte@fraud-detection.com
- Issues: GitHub Issues

## 🔄 Changelog

### v1.0.0
- Implementación inicial del sistema
- 5 modelos de ML integrados
- API REST con FastAPI
- Integración con Kafka y PostgreSQL
- Dockerización completa
