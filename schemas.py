"""
Esquemas Pydantic para validación de datos de entrada y salida.
Define la estructura de datos esperada para transacciones y predicciones.
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Union
import numpy as np


class TransactionInput(BaseModel):
    """
    Esquema para datos de entrada de transacciones.
    Valida la estructura y tipos de datos requeridos.
    """
    transaction_id: str = Field(..., description="Identificador único de la transacción")
    amount: Optional[float] = Field(0.0, description="Monto de la transacción")
    time: Optional[float] = Field(0.0, description="Timestamp de la transacción")
    
    # Variables V1-V28 (features del modelo)
    v1: Optional[float] = Field(0.0, description="Variable V1")
    v2: Optional[float] = Field(0.0, description="Variable V2")
    v3: Optional[float] = Field(0.0, description="Variable V3")
    v4: Optional[float] = Field(0.0, description="Variable V4")
    v5: Optional[float] = Field(0.0, description="Variable V5")
    v6: Optional[float] = Field(0.0, description="Variable V6")
    v7: Optional[float] = Field(0.0, description="Variable V7")
    v8: Optional[float] = Field(0.0, description="Variable V8")
    v9: Optional[float] = Field(0.0, description="Variable V9")
    v10: Optional[float] = Field(0.0, description="Variable V10")
    v11: Optional[float] = Field(0.0, description="Variable V11")
    v12: Optional[float] = Field(0.0, description="Variable V12")
    v13: Optional[float] = Field(0.0, description="Variable V13")
    v14: Optional[float] = Field(0.0, description="Variable V14")
    v15: Optional[float] = Field(0.0, description="Variable V15")
    v16: Optional[float] = Field(0.0, description="Variable V16")
    v17: Optional[float] = Field(0.0, description="Variable V17")
    v18: Optional[float] = Field(0.0, description="Variable V18")
    v19: Optional[float] = Field(0.0, description="Variable V19")
    v20: Optional[float] = Field(0.0, description="Variable V20")
    v21: Optional[float] = Field(0.0, description="Variable V21")
    v22: Optional[float] = Field(0.0, description="Variable V22")
    v23: Optional[float] = Field(0.0, description="Variable V23")
    v24: Optional[float] = Field(0.0, description="Variable V24")
    v25: Optional[float] = Field(0.0, description="Variable V25")
    v26: Optional[float] = Field(0.0, description="Variable V26")
    v27: Optional[float] = Field(0.0, description="Variable V27")
    v28: Optional[float] = Field(0.0, description="Variable V28")

    @validator('amount')
    def validate_amount(cls, v):
        """Valida que el monto sea positivo."""
        if v is not None and v < 0:
            raise ValueError('El monto debe ser positivo')
        return v

    @validator('time')
    def validate_time(cls, v):
        """Valida que el tiempo sea un timestamp válido."""
        if v is not None and v < 0:
            raise ValueError('El tiempo debe ser un timestamp válido')
        return v

    @validator('transaction_id')
    def validate_transaction_id(cls, v):
        """Valida que el ID de transacción no esté vacío."""
        if not v or not v.strip():
            raise ValueError('El ID de transacción no puede estar vacío')
        return v.strip()

    class Config:
        """Configuración del esquema."""
        schema_extra = {
            "example": {
                "transaction_id": "TXN_12345",
                "amount": 100.50,
                "time": 1234567890.0,
                "v1": 0.1,
                "v2": 0.2,
                "v3": 0.3,
                "v4": 0.4,
                "v5": 0.5,
                "v6": 0.6,
                "v7": 0.7,
                "v8": 0.8,
                "v9": 0.9,
                "v10": 0.10,
                "v11": 0.11,
                "v12": 0.12,
                "v13": 0.13,
                "v14": 0.14,
                "v15": 0.15,
                "v16": 0.16,
                "v17": 0.17,
                "v18": 0.18,
                "v19": 0.19,
                "v20": 0.20,
                "v21": 0.21,
                "v22": 0.22,
                "v23": 0.23,
                "v24": 0.24,
                "v25": 0.25,
                "v26": 0.26,
                "v27": 0.27,
                "v28": 0.28
            }
        }


class ModelPrediction(BaseModel):
    """
    Esquema para predicciones individuales de cada modelo.
    """
    non_fraud: float = Field(..., ge=0.0, le=1.0, description="Probabilidad de no fraude")
    fraud: float = Field(..., ge=0.0, le=1.0, description="Probabilidad de fraude")

    @validator('non_fraud', 'fraud')
    def validate_probabilities(cls, v):
        """Valida que las probabilidades estén entre 0 y 1."""
        if not 0.0 <= v <= 1.0:
            raise ValueError('Las probabilidades deben estar entre 0 y 1')
        return round(v, 4)

    @validator('fraud')
    def validate_probability_sum(cls, v, values):
        """Valida que la suma de probabilidades sea aproximadamente 1."""
        if 'non_fraud' in values:
            total = values['non_fraud'] + v
            if abs(total - 1.0) > 0.01:
                raise ValueError('La suma de probabilidades debe ser aproximadamente 1')
        return v


class ModelPredictionArray(BaseModel):
    """
    Esquema para predicciones en formato de array [non_fraud, fraud].
    """
    predictions: List[float] = Field(..., min_items=2, max_items=2, description="Array [non_fraud, fraud]")

    @validator('predictions')
    def validate_predictions(cls, v):
        """Valida que el array tenga exactamente 2 elementos y que sean probabilidades válidas."""
        if len(v) != 2:
            raise ValueError('Debe tener exactamente 2 elementos')
        
        non_fraud, fraud = v
        if not (0.0 <= non_fraud <= 1.0 and 0.0 <= fraud <= 1.0):
            raise ValueError('Las probabilidades deben estar entre 0 y 1')
        
        if abs(non_fraud + fraud - 1.0) > 0.01:
            raise ValueError('La suma de probabilidades debe ser aproximadamente 1')
        
        return [round(non_fraud, 4), round(fraud, 4)]


class PredictionResponse(BaseModel):
    """
    Esquema para la respuesta completa de predicciones.
    """
    transaction_id: str = Field(..., description="ID de la transacción procesada")
    logistic: ModelPredictionArray = Field(..., description="Predicciones del modelo de regresión logística")
    kneighbors: ModelPredictionArray = Field(..., description="Predicciones del modelo K-Nearest Neighbors")
    svc: ModelPrediction = Field(..., description="Predicciones del modelo Support Vector Classifier")
    tree: ModelPredictionArray = Field(..., description="Predicciones del modelo de árbol de decisión")
    keras: ModelPrediction = Field(..., description="Predicciones del modelo Keras")

    class Config:
        """Configuración del esquema."""
        schema_extra = {
            "example": {
                "transaction_id": "TXN_12345",
                "logistic": [0.8, 0.2],
                "kneighbors": [0.7, 0.3],
                "svc": {"non_fraud": 0.6, "fraud": 0.4},
                "tree": [0.9, 0.1],
                "keras": {"non_fraud": 0.75, "fraud": 0.25}
            }
        }


class TransactionResult(BaseModel):
    """
    Esquema para el resultado final de una transacción.
    """
    transaction_id: str = Field(..., description="ID de la transacción")
    status: str = Field(..., description="Estado de la transacción (fraude/aprobada/sin resultado)")
    details: Dict[str, Union[Dict, List]] = Field(..., description="Detalles completos de la transacción")

    @validator('status')
    def validate_status(cls, v):
        """Valida que el status sea uno de los valores permitidos."""
        allowed_statuses = ['fraude', 'aprobada', 'sin resultado']
        if v not in allowed_statuses:
            raise ValueError(f'Status debe ser uno de: {allowed_statuses}')
        return v

    class Config:
        """Configuración del esquema."""
        schema_extra = {
            "example": {
                "transaction_id": "TXN_12345",
                "status": "aprobada",
                "details": {
                    "transaction_json": {"amount": 100.50, "time": 1234567890},
                    "logistic": [0.8, 0.2],
                    "kneighbors": [0.7, 0.3],
                    "svc": {"non_fraud": 0.6, "fraud": 0.4},
                    "tree": [0.9, 0.1],
                    "keras": {"non_fraud": 0.75, "fraud": 0.25}
                }
            }
        }


class HealthResponse(BaseModel):
    """
    Esquema para la respuesta del endpoint de salud.
    """
    status: str = Field(..., description="Estado de la aplicación")
    timestamp: str = Field(..., description="Timestamp de la verificación")
    version: str = Field(..., description="Versión de la aplicación")
    models_loaded: bool = Field(..., description="Indica si los modelos están cargados")
    database_connected: bool = Field(..., description="Indica si la base de datos está conectada")
    kafka_connected: bool = Field(..., description="Indica si Kafka está conectado")

    class Config:
        """Configuración del esquema."""
        schema_extra = {
            "example": {
                "status": "ok",
                "timestamp": "2025-08-30T10:30:00Z",
                "version": "1.0.0",
                "models_loaded": True,
                "database_connected": True,
                "kafka_connected": True
            }
        }


class ErrorResponse(BaseModel):
    """
    Esquema para respuestas de error.
    """
    error: str = Field(..., description="Descripción del error")
    detail: Optional[str] = Field(None, description="Detalles adicionales del error")
    timestamp: str = Field(..., description="Timestamp del error")

    class Config:
        """Configuración del esquema."""
        schema_extra = {
            "example": {
                "error": "Transacción no encontrada",
                "detail": "La transacción con ID TXN_12345 no existe en la base de datos",
                "timestamp": "2025-08-30T10:30:00Z"
            }
        }
