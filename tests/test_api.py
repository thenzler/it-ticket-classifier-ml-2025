#!/usr/bin/env python3
"""
API Tests für IT-Ticket Classification System

ATL - HF Wirtschaftsinformatik
Autor: Benjamin Peter
Datum: 08.06.2025
"""

import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from api.main import app
except ImportError:
    pytest.skip("API module not available", allow_module_level=True)

client = TestClient(app)

class TestAPI:
    """Test Suite für FastAPI Endpoints"""
    
    def test_root_endpoint(self):
        """Test Root Endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "2.1.3"
    
    def test_health_endpoint(self):
        """Test Health Check Endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert "model_loaded" in data
        assert "timestamp" in data
    
    def test_model_info_endpoint(self):
        """Test Model Info Endpoint"""
        response = client.get("/api/v1/model-info")
        # Kann 503 sein wenn Modell nicht geladen
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "model_version" in data
            assert "supported_categories" in data
            assert "supported_priorities" in data
    
    def test_statistics_endpoint(self):
        """Test Statistics Endpoint"""
        response = client.get("/api/v1/statistics")
        assert response.status_code == 200
        data = response.json()
        assert "daily_stats" in data
        assert "category_breakdown" in data
        assert "priority_breakdown" in data
    
    def test_classify_ticket_endpoint_structure(self):
        """Test Classify Ticket Endpoint Struktur"""
        # Test mit gültigem Ticket
        ticket_data = {
            "title": "Test laptop issue",
            "description": "Laptop won't start properly",
            "user_role": "end_user",
            "department": "Finance",
            "affected_system": "workstation",
            "hour_submitted": 14,
            "is_weekend": 0,
            "previous_tickets_30d": 1
        }
        
        response = client.post("/api/v1/classify-ticket", json=ticket_data)
        
        # Kann 503 sein wenn Modell nicht geladen, 200 wenn erfolgreich
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "prediction" in data
            assert "routing" in data
            assert "explanation" in data
            assert "metadata" in data
            
            # Prüfe Prediction Struktur
            prediction = data["prediction"]
            assert "category" in prediction
            assert "priority" in prediction
            assert "category_confidence" in prediction
            assert "priority_confidence" in prediction
            assert "overall_confidence" in prediction
    
    def test_classify_ticket_invalid_data(self):
        """Test Classify Ticket mit ungültigen Daten"""
        # Test mit fehlendem Feld
        invalid_ticket = {
            "title": "Test",
            "description": "Test description"
            # Fehlende Pflichtfelder
        }
        
        response = client.post("/api/v1/classify-ticket", json=invalid_ticket)
        assert response.status_code == 422  # Validation Error
    
    def test_openapi_docs(self):
        """Test ob OpenAPI Dokumentation verfügbar ist"""
        response = client.get("/docs")
        assert response.status_code == 200
        
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        openapi_data = response.json()
        assert "openapi" in openapi_data
        assert "info" in openapi_data
        assert openapi_data["info"]["title"] == "IT-Ticket Classification API"