"""
Tests unitarios para el módulo de predicción.
"""

import pytest
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prediction import process_transaction, load_models


class TestPrediction:
    """Tests para el módulo de predicción."""
    
    @pytest.fixture
    def sample_transaction(self):
        """Transacción de ejemplo para testing."""
        return {
            "transaction_id": "TEST_123",
            "amount": 100.0,
            "time": 1234567890.0,
            "v1": 0.1, "v2": 0.2, "v3": 0.3, "v4": 0.4, "v5": 0.5,
            "v6": 0.6, "v7": 0.7, "v8": 0.8, "v9": 0.9, "v10": 0.10,
            "v11": 0.11, "v12": 0.12, "v13": 0.13, "v14": 0.14, "v15": 0.15,
            "v16": 0.16, "v17": 0.17, "v18": 0.18, "v19": 0.19, "v20": 0.20,
            "v21": 0.21, "v22": 0.22, "v23": 0.23, "v24": 0.24, "v25": 0.25,
            "v26": 0.26, "v27": 0.27, "v28": 0.28
        }
    
    @pytest.fixture
    def mock_models(self):
        """Modelos mock para testing."""
        models = {}
        
        # Mock para regresión logística
        mock_logistic = Mock()
        mock_logistic.predict_proba.return_value = np.array([[0.8, 0.2]])
        models['logistic'] = mock_logistic
        
        # Mock para k-neighbors
        mock_kneighbors = Mock()
        mock_kneighbors.predict_proba.return_value = np.array([[0.7, 0.3]])
        models['kneighbors'] = mock_kneighbors
        
        # Mock para SVC
        mock_svc = Mock()
        mock_svc.decision_function.return_value = np.array([0.5])
        models['svc'] = mock_svc
        
        # Mock para árbol de decisión
        mock_tree = Mock()
        mock_tree.predict_proba.return_value = np.array([[0.9, 0.1]])
        models['tree'] = mock_tree
        
        # Mock para Keras
        mock_keras = Mock()
        mock_keras.predict.return_value = np.array([[0.75, 0.25]])
        models['keras'] = mock_keras
        
        return models
    
    def test_process_transaction_valid_input(self, sample_transaction, mock_models):
        """Test procesamiento de transacción con entrada válida."""
        predictions = process_transaction(sample_transaction, mock_models)
        
        # Verificar estructura de respuesta
        assert 'logistic' in predictions
        assert 'kneighbors' in predictions
        assert 'svc' in predictions
        assert 'tree' in predictions
        assert 'keras' in predictions
        
        # Verificar tipos de datos
        assert isinstance(predictions['logistic'], list)
        assert len(predictions['logistic']) == 2
        assert all(isinstance(x, float) for x in predictions['logistic'])
        
        assert isinstance(predictions['svc'], dict)
        assert 'fraud' in predictions['svc']
        assert 'non_fraud' in predictions['svc']
        assert all(isinstance(x, float) for x in predictions['svc'].values())
    
    def test_process_transaction_missing_amount(self, mock_models):
        """Test procesamiento con monto faltante."""
        transaction = {
            "transaction_id": "TEST_123",
            "time": 1234567890.0,
            "v1": 0.1, "v2": 0.2, "v3": 0.3, "v4": 0.4, "v5": 0.5,
            "v6": 0.6, "v7": 0.7, "v8": 0.8, "v9": 0.9, "v10": 0.10,
            "v11": 0.11, "v12": 0.12, "v13": 0.13, "v14": 0.14, "v15": 0.15,
            "v16": 0.16, "v17": 0.17, "v18": 0.18, "v19": 0.19, "v20": 0.20,
            "v21": 0.21, "v22": 0.22, "v23": 0.23, "v24": 0.24, "v25": 0.25,
            "v26": 0.26, "v27": 0.27, "v28": 0.28
        }
        
        predictions = process_transaction(transaction, mock_models)
        assert predictions is not None
        assert 'logistic' in predictions
    
    def test_process_transaction_missing_time(self, mock_models):
        """Test procesamiento con tiempo faltante."""
        transaction = {
            "transaction_id": "TEST_123",
            "amount": 100.0,
            "v1": 0.1, "v2": 0.2, "v3": 0.3, "v4": 0.4, "v5": 0.5,
            "v6": 0.6, "v7": 0.7, "v8": 0.8, "v9": 0.9, "v10": 0.10,
            "v11": 0.11, "v12": 0.12, "v13": 0.13, "v14": 0.14, "v15": 0.15,
            "v16": 0.16, "v17": 0.17, "v18": 0.18, "v19": 0.19, "v20": 0.20,
            "v21": 0.21, "v22": 0.22, "v23": 0.23, "v24": 0.24, "v25": 0.25,
            "v26": 0.26, "v27": 0.27, "v28": 0.28
        }
        
        predictions = process_transaction(transaction, mock_models)
        assert predictions is not None
        assert 'logistic' in predictions
    
    def test_process_transaction_minimal_input(self, mock_models):
        """Test procesamiento con entrada mínima."""
        transaction = {
            "transaction_id": "TEST_123"
        }
        
        predictions = process_transaction(transaction, mock_models)
        assert predictions is not None
        assert 'logistic' in predictions
    
    @patch('prediction.joblib.load')
    @patch('prediction.load_model')
    def test_load_models_success(self, mock_load_model, mock_joblib_load):
        """Test carga exitosa de modelos."""
        # Mock para joblib.load
        mock_logistic = Mock()
        mock_kneighbors = Mock()
        mock_svc = Mock()
        mock_tree = Mock()
        
        mock_joblib_load.side_effect = [mock_logistic, mock_kneighbors, mock_svc, mock_tree]
        
        # Mock para load_model
        mock_keras = Mock()
        mock_keras.compile.return_value = None
        mock_load_model.return_value = mock_keras
        
        models = load_models()
        
        assert 'logistic' in models
        assert 'kneighbors' in models
        assert 'svc' in models
        assert 'tree' in models
        assert 'keras' in models
    
    def test_process_transaction_probability_ranges(self, sample_transaction, mock_models):
        """Test que las probabilidades estén en el rango correcto."""
        predictions = process_transaction(sample_transaction, mock_models)
        
        # Verificar que las probabilidades estén entre 0 y 1
        for model_name, prediction in predictions.items():
            if isinstance(prediction, list):
                assert all(0 <= p <= 1 for p in prediction)
            elif isinstance(prediction, dict):
                assert all(0 <= p <= 1 for p in prediction.values())
    
    def test_process_transaction_probability_sum(self, sample_transaction, mock_models):
        """Test que la suma de probabilidades sea aproximadamente 1."""
        predictions = process_transaction(sample_transaction, mock_models)
        
        # Verificar suma de probabilidades
        for model_name, prediction in predictions.items():
            if isinstance(prediction, list):
                assert abs(sum(prediction) - 1.0) < 0.01
            elif isinstance(prediction, dict):
                assert abs(sum(prediction.values()) - 1.0) < 0.01


if __name__ == "__main__":
    pytest.main([__file__])
