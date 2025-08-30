# 🛒 Simulador de Compras en Línea con Detección de Fraude

## Descripción

Esta aplicación Streamlit simula transacciones de compras en línea y las envía a un sistema de detección de fraude en tiempo real utilizando Apache Kafka y FastAPI.

## Características

- 🛍️ **Simulación de Compras**: Genera transacciones aleatorias con datos realistas
- 🔍 **Detección de Fraude**: Integración con sistema de ML para detectar transacciones fraudulentas
- 📊 **Tiempo Real**: Procesamiento en tiempo real usando Apache Kafka
- 🐳 **Containerizado**: Listo para desplegar con Docker

## Tecnologías Utilizadas

- **Frontend**: Streamlit
- **Mensajería**: Apache Kafka (Confluent)
- **API**: FastAPI
- **Containerización**: Docker
- **Lenguaje**: Python 3.9

## Configuración

### Variables de Entorno

Crea un archivo `.env` con las siguientes variables:

```env
KAFKA_BROKER=your-kafka-broker
KAFKA_USERNAME=your-kafka-username
KAFKA_PASSWORD=your-kafka-password
KAFKA_TOPIC_INPUT=your-input-topic
ENDPOINT=your-fastapi-endpoint
```

### Instalación Local

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Ejecución con Docker

```bash
docker build -t fraud-simulator .
docker run -p 8501:8501 fraud-simulator
```

## Uso

1. Abre la aplicación en tu navegador (http://localhost:8501)
2. Ingresa un ID de usuario (opcional)
3. Define el monto de la compra
4. Haz clic en "Comprar Ahora"
5. Espera el resultado de la detección de fraude

## Estructura del Proyecto

```
front_streamlit/
├── app.py              # Aplicación principal Streamlit
├── requirements.txt    # Dependencias de Python
├── Dockerfile         # Configuración de Docker
└── README.md          # Documentación
```

## Rama Actual

Esta es la rama `front-streamlit` del proyecto `proyectfraudarlex`, que contiene la interfaz de usuario para simular transacciones y visualizar resultados de detección de fraude.
