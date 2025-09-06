import streamlit as st
import random
import json
import os
import logging
import time
import requests
from dotenv import load_dotenv
from confluent_kafka import Producer

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de Kafka obtenida desde variables de entorno
KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_USERNAME = os.getenv("KAFKA_USERNAME")
KAFKA_PASSWORD = os.getenv("KAFKA_PASSWORD")
KAFKA_TOPIC_INPUT = os.getenv("KAFKA_TOPIC_INPUT")
ENDPOINT = os.getenv("ENDPOINT", "https://proyectfraudarlex-1.onrender.com")

# Configuración para el Producer de Confluent Kafka
producer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': KAFKA_USERNAME,
    'sasl.password': KAFKA_PASSWORD,
    'client.id': 'streamlit-producer',
    'acks': 'all',
    'retries': 3,
    'batch.size': 16384,
    'linger.ms': 1,
}

# Crear el Producer
try:
    producer = Producer(producer_conf)
    logger.info("Producer creado correctamente.")
except Exception as e:
    logger.error("Error al crear el Producer: %s", e)
    st.error("Error al inicializar el Kafka Producer.")


# Función para generar una transacción aleatoria
def generar_transaccion():
    return {
        "transaction_id": f"TX{random.randint(10000, 99999)}",
        "user_id": f"U{random.randint(100, 999)}",
        "time": round(random.uniform(1, 172792), 2),
        "amount": round(random.uniform(1, 500), 2),
        "V1": random.uniform(-3, 3),
        "V2": random.uniform(-3, 3),
        "V3": random.uniform(-3, 3),
        "V4": random.uniform(-3, 3),
        "V5": random.uniform(-3, 3),
        "V6": random.uniform(-3, 3),
        "V7": random.uniform(-3, 3),
        "V8": random.uniform(-3, 3),
        "V9": random.uniform(-3, 3),
        "V10": random.uniform(-3, 3),
        "V11": random.uniform(-3, 3),
        "V12": random.uniform(-3, 3),
        "V13": random.uniform(-3, 3),
        "V14": random.uniform(-3, 3),
        "V15": random.uniform(-3, 3),
        "V16": random.uniform(-3, 3),
        "V17": random.uniform(-3, 3),
        "V18": random.uniform(-3, 3),
        "V19": random.uniform(-3, 3),
        "V20": random.uniform(-3, 3),
        "V21": random.uniform(-3, 3),
        "V22": random.uniform(-3, 3),
        "V23": random.uniform(-3, 3),
        "V24": random.uniform(-3, 3),
        "V25": random.uniform(-3, 3),
        "V26": random.uniform(-3, 3),
        "V27": random.uniform(-3, 3),
        "V28": random.uniform(-3, 3),
    }


# Configuración de la interfaz de Streamlit
st.title("🛒 Simulador de Compras en Línea con Detección de Fraude")
st.write("Realiza una compra y verifica si es detectada como fraude o no.")

st.subheader("🛍️ Realiza una Compra")
usuario = st.text_input("ID del Usuario (opcional)", f"U{random.randint(100, 999)}")
monto = st.number_input("Monto de la compra ($) (opcional)", min_value=1.0, max_value=500.0, value=50.0, step=5.0)
realizar_compra = st.button("Comprar Ahora")

if realizar_compra:
    # Generar la transacción
    transaccion = generar_transaccion()
    st.json(transaccion)

    # Enviar la transacción a Kafka utilizando el Producer
    try:
        producer.produce(
            KAFKA_TOPIC_INPUT,
            key=transaccion["transaction_id"],
            value=json.dumps(transaccion)
        )
        producer.flush()  # Envío inmediato
        st.success("📤 Transacción enviada a Kafka.")
        logger.info("Transacción enviada: %s", transaccion)
    except Exception as e:
        logger.error("Error al enviar la transacción: %s", e)
        st.error("Error al enviar la transacción a Kafka.")

    # Esperar la respuesta del modelo a través del endpoint de FastAPI mediante polling
    st.subheader("🔍 Esperando resultado de la predicción...")
    
    api_url = f'{ENDPOINT}/transaction/{transaccion["transaction_id"]}'

    timeout = 30  # segundos máximos de espera
    interval = 2  # intervalo de consulta en segundos
    start_time = time.time()
    data = None
    attempts = 0
    max_attempts = timeout // interval

    # Crear un placeholder para mostrar el progreso
    progress_bar = st.progress(0)
    status_text = st.empty()

    while attempts < max_attempts:
        attempts += 1
        progress = attempts / max_attempts
        progress_bar.progress(progress)
        status_text.text(f"Intento {attempts}/{max_attempts} - Consultando API...")
        
        try:
            response = requests.get(api_url, timeout=10)
            logger.info(f"Respuesta del API - Status: {response.status_code}, Intento: {attempts}")
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Datos recibidos: {data}")
                break
            elif response.status_code == 404:
                status_text.text(f"Transacción no encontrada aún (404) - Intento {attempts}/{max_attempts}")
                logger.info(f"Transacción no encontrada: {transaccion['transaction_id']}")
            else:
                status_text.text(f"Error del servidor ({response.status_code}) - Intento {attempts}/{max_attempts}")
                logger.warning(f"Error del servidor: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            status_text.text(f"Error de conexión - Intento {attempts}/{max_attempts}")
            logger.error(f"Error de conexión: {e}")
        
        if attempts < max_attempts:
            time.sleep(interval)

    progress_bar.progress(1.0)
    
    if data is None:
        st.error("❌ No se pudo obtener el resultado de la predicción.")
        st.warning("**Posibles causas:**")
        st.write("• El endpoint `/transaction/{id}` no está implementado en el backend")
        st.write("• El backend no está procesando las transacciones de Kafka")
        st.write("• El modelo de ML no está funcionando correctamente")
        st.write("• Problemas de sincronización entre frontend y backend")
        st.write("• El backend está en otra rama y no está desplegado")
        
        st.info("**Solución sugerida:**")
        st.write("1. Verificar que el backend esté desplegado y funcionando")
        st.write("2. Implementar el endpoint `/transaction/{id}` en el backend")
        st.write("3. Asegurar que el procesamiento de Kafka esté funcionando")
        st.write("4. Verificar la configuración de variables de entorno")
    else:
        status_text.text("✅ Resultado obtenido!")
        if data["status"] == "fraude":
            st.error("⚠️ FRAUDE DETECTADO - Esta transacción es sospechosa.")
        elif data["status"] == "aprobada":
            st.success("✅ Transacción Aprobada - Compra exitosa.")
        else:
            st.warning("Transacción en proceso o sin resultado definitivo.")
        
        # Mostrar datos completos de la respuesta
        with st.expander("📊 Detalles de la respuesta"):
            st.json(data)