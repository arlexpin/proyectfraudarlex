"""
Configuración centralizada de logging para la aplicación.
Define formatos, niveles y handlers para diferentes entornos.
"""

import logging
import logging.config
import os
from datetime import datetime
from typing import Dict, Any


def get_logging_config() -> Dict[str, Any]:
    """
    Retorna la configuración de logging según el entorno.
    
    Returns:
        Dict[str, Any]: Configuración de logging
    """
    environment = os.getenv('ENVIRONMENT', 'development')
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    # Configuración base
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s - %(message)s'
            },
            'json': {
                'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}',
                'datefmt': '%Y-%m-%dT%H:%M:%SZ'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': 'simple' if environment == 'development' else 'detailed',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': log_level,
                'formatter': 'detailed',
                'filename': 'logs/app.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            },
            'error_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'ERROR',
                'formatter': 'detailed',
                'filename': 'logs/error.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            }
        },
        'loggers': {
            '': {  # Root logger
                'level': log_level,
                'handlers': ['console', 'file', 'error_file'],
                'propagate': False
            },
            'main': {
                'level': log_level,
                'handlers': ['console', 'file', 'error_file'],
                'propagate': False
            },
            'prediction': {
                'level': log_level,
                'handlers': ['console', 'file', 'error_file'],
                'propagate': False
            },
            'db': {
                'level': log_level,
                'handlers': ['console', 'file', 'error_file'],
                'propagate': False
            },
            'kafka_client': {
                'level': log_level,
                'handlers': ['console', 'file', 'error_file'],
                'propagate': False
            },
            'uvicorn': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
                'propagate': False
            },
            'uvicorn.access': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
                'propagate': False
            }
        }
    }
    
    # Configuración específica para producción
    if environment == 'production':
        config['formatters']['json']['format'] = (
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
            '"logger": "%(name)s", "message": "%(message)s", '
            '"module": "%(module)s", "function": "%(funcName)s", '
            '"line": "%(lineno)d"}'
        )
        config['handlers']['console']['formatter'] = 'json'
        config['handlers']['file']['formatter'] = 'json'
        config['handlers']['error_file']['formatter'] = 'json'
    
    return config


def setup_logging():
    """
    Configura el sistema de logging de la aplicación.
    Crea el directorio de logs si no existe.
    """
    # Crear directorio de logs si no existe
    os.makedirs('logs', exist_ok=True)
    
    # Aplicar configuración
    logging.config.dictConfig(get_logging_config())
    
    # Log de inicio
    logger = logging.getLogger(__name__)
    logger.info("Sistema de logging configurado correctamente")
    logger.info(f"Entorno: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"Nivel de log: {os.getenv('LOG_LEVEL', 'INFO')}")


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger configurado para el módulo especificado.
    
    Args:
        name (str): Nombre del módulo/logger
        
    Returns:
        logging.Logger: Logger configurado
    """
    return logging.getLogger(name)


# Configuración automática al importar el módulo
setup_logging()


# Funciones de utilidad para logging
def log_transaction_processing(transaction_id: str, processing_time: float, success: bool):
    """
    Registra información sobre el procesamiento de una transacción.
    
    Args:
        transaction_id (str): ID de la transacción
        processing_time (float): Tiempo de procesamiento en segundos
        success (bool): Si el procesamiento fue exitoso
    """
    logger = get_logger('main')
    status = "exitoso" if success else "fallido"
    logger.info(f"Procesamiento de transacción {transaction_id}: {status} en {processing_time:.3f}s")


def log_model_prediction(model_name: str, transaction_id: str, prediction: dict):
    """
    Registra las predicciones de un modelo específico.
    
    Args:
        model_name (str): Nombre del modelo
        transaction_id (str): ID de la transacción
        prediction (dict): Predicciones del modelo
    """
    logger = get_logger('prediction')
    logger.info(f"Modelo {model_name} - Transacción {transaction_id}: {prediction}")


def log_database_operation(operation: str, table: str, success: bool, details: str = None):
    """
    Registra operaciones de base de datos.
    
    Args:
        operation (str): Tipo de operación (INSERT, SELECT, etc.)
        table (str): Nombre de la tabla
        success (bool): Si la operación fue exitosa
        details (str): Detalles adicionales
    """
    logger = get_logger('db')
    status = "exitoso" if success else "fallido"
    message = f"Operación {operation} en tabla {table}: {status}"
    if details:
        message += f" - {details}"
    
    if success:
        logger.info(message)
    else:
        logger.error(message)


def log_kafka_operation(operation: str, topic: str, success: bool, details: str = None):
    """
    Registra operaciones de Kafka.
    
    Args:
        operation (str): Tipo de operación (PRODUCE, CONSUME, etc.)
        topic (str): Nombre del tópico
        success (bool): Si la operación fue exitosa
        details (str): Detalles adicionales
    """
    logger = get_logger('kafka_client')
    status = "exitoso" if success else "fallido"
    message = f"Operación {operation} en tópico {topic}: {status}"
    if details:
        message += f" - {details}"
    
    if success:
        logger.info(message)
    else:
        logger.error(message)


def log_application_startup():
    """
    Registra el inicio de la aplicación.
    """
    logger = get_logger('main')
    logger.info("=" * 50)
    logger.info("INICIANDO SISTEMA DE DETECCIÓN DE FRAUDE")
    logger.info("=" * 50)
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info(f"Entorno: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"Versión: {os.getenv('APP_VERSION', '1.0.0')}")


def log_application_shutdown():
    """
    Registra el cierre de la aplicación.
    """
    logger = get_logger('main')
    logger.info("=" * 50)
    logger.info("CERRANDO SISTEMA DE DETECCIÓN DE FRAUDE")
    logger.info("=" * 50)
    logger.info(f"Timestamp: {datetime.now().isoformat()}")


# Configuración para desarrollo local
if __name__ == "__main__":
    # Ejemplo de uso
    setup_logging()
    
    logger = get_logger(__name__)
    logger.info("Ejemplo de logging configurado")
    logger.warning("Este es un warning de ejemplo")
    logger.error("Este es un error de ejemplo")
    
    # Ejemplos de logging específico
    log_transaction_processing("TXN_12345", 0.150, True)
    log_model_prediction("logistic", "TXN_12345", {"fraud": 0.2, "non_fraud": 0.8})
    log_database_operation("INSERT", "transactions", True, "Transacción almacenada")
    log_kafka_operation("PRODUCE", "fraud_predictions", True, "Predicción enviada")
