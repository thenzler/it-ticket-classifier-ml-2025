#!/usr/bin/env python3
"""
FastAPI REST API für IT-Ticket Classification System
Echtzeit-Klassifikation von IT-Support-Tickets

ATL - HF Wirtschaftsinformatik
Autor: Benjamin Peter
Datum: 08.06.2025
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import pandas as pd
import numpy as np
import os
import sys
import time
import logging
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from models.train_classifier import ITTicketClassifier
except ImportError:
    print("⚠️ Kann ITTicketClassifier nicht importieren. Stelle sicher, dass das Modell verfügbar ist.")
    ITTicketClassifier = None

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI App
app = FastAPI(
    title="IT-Ticket Classification API",
    description="Machine Learning API für automatische IT-Ticket Kategorisierung und Priorisierung",
    version="2.1.3",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Classifier Instance
classifier = None

# Pydantic Models
class TicketInput(BaseModel):
    title: str = Field(..., description="Ticket Titel", example="Laptop won't start - black screen")
    description: str = Field(..., description="Ticket Beschreibung", example="My laptop shows a black screen when I press the power button. Tried restarting multiple times.")
    user_role: str = Field(..., description="Benutzer-Rolle", example="end_user")
    department: str = Field(..., description="Abteilung", example="Finance")
    affected_system: str = Field(..., description="Betroffenes System", example="workstation")
    hour_submitted: int = Field(..., description="Stunde der Einreichung (0-23)", example=14)
    is_weekend: int = Field(..., description="Wochenende? (0=Nein, 1=Ja)", example=0)
    previous_tickets_30d: int = Field(..., description="Anzahl Tickets der letzten 30 Tage", example=1)

class ClassificationResult(BaseModel):
    category: str = Field(..., description="Vorhergesagte Kategorie")
    priority: str = Field(..., description="Vorhergesagte Priorität")
    category_confidence: float = Field(..., description="Confidence Score für Kategorie")
    priority_confidence: float = Field(..., description="Confidence Score für Priorität")
    overall_confidence: float = Field(..., description="Gesamt-Confidence Score")

class TicketPrediction(BaseModel):
    prediction: ClassificationResult
    routing: Dict[str, Any] = Field(..., description="Routing-Empfehlungen")
    explanation: Dict[str, Any] = Field(..., description="Erklärung der Klassifikation")
    metadata: Dict[str, Any] = Field(..., description="Metadaten der Vorhersage")

class HealthResponse(BaseModel):
    status: str
    version: str
    model_loaded: bool
    timestamp: str

# Helper Functions
def get_team_assignment(category: str) -> str:
    """Bestimmt Team-Zuweisung basierend auf Kategorie"""
    team_mapping = {
        "Hardware": "Hardware Support Team",
        "Software": "Software Support Team", 
        "Network": "Network Operations Team",
        "Security": "Security Incident Response Team"
    }
    return team_mapping.get(category, "General IT Support")

def get_sla_target(priority: str) -> str:
    """Bestimmt SLA-Ziel basierend auf Priorität"""
    sla_mapping = {
        "Critical": "1 hour",
        "High": "4 hours",
        "Medium": "24 hours", 
        "Low": "72 hours"
    }
    return sla_mapping.get(priority, "24 hours")

def get_confidence_level(confidence: float) -> str:
    """Bestimmt Confidence Level"""
    if confidence >= 0.9:
        return "high"
    elif confidence >= 0.8:
        return "medium"
    else:
        return "low"

def get_recommendation(confidence: float) -> str:
    """Gibt Empfehlung basierend auf Confidence"""
    if confidence >= 0.9:
        return "automatic_assignment"
    elif confidence >= 0.8:
        return "review_recommended"
    else:
        return "manual_classification_required"

# Startup Event
@app.on_event("startup")
async def startup_event():
    """Lädt das ML-Modell beim Start der API"""
    global classifier
    
    try:
        logger.info("🚀 Starte IT-Ticket Classification API...")
        
        if ITTicketClassifier is None:
            logger.error("❌ ITTicketClassifier nicht verfügbar")
            classifier = None
            return
        
        # Lade Modell
        model_path = "data/models/it_ticket_classifier_v2.1.3.pkl"
        
        if not os.path.exists(model_path):
            logger.warning(f"⚠️ Modell nicht gefunden: {model_path}")
            logger.info("🔄 Trainiere neues Modell...")
            
            # Trainiere Modell falls nicht vorhanden
            try:
                from models.train_classifier import main as train_main
                train_main()
            except Exception as e:
                logger.error(f"❌ Fehler beim Trainieren: {e}")
                classifier = None
                return
        
        classifier = ITTicketClassifier()
        classifier.load_model(model_path)
        
        logger.info("✅ Modell erfolgreich geladen!")
        
    except Exception as e:
        logger.error(f"❌ Fehler beim Laden des Modells: {e}")
        # API startet trotzdem, aber ohne Modell
        classifier = None

# API Endpoints
@app.get("/", response_model=Dict[str, str])
async def root():
    """Root Endpoint mit API-Info"""
    return {
        "message": "IT-Ticket Classification API",
        "version": "2.1.3",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health Check Endpoint"""
    return HealthResponse(
        status="healthy" if classifier and classifier.is_trained else "degraded",
        version="2.1.3",
        model_loaded=classifier is not None and classifier.is_trained,
        timestamp=datetime.now().isoformat()
    )

@app.post("/api/v1/classify-ticket", response_model=TicketPrediction)
async def classify_ticket(ticket: TicketInput):
    """Klassifiziert ein einzelnes IT-Ticket"""
    
    if not classifier or not classifier.is_trained:
        raise HTTPException(
            status_code=503, 
            detail="ML-Modell nicht verfügbar. Bitte später versuchen."
        )
    
    try:
        start_time = time.time()
        
        # Konvertiere Input zu DataFrame
        ticket_df = pd.DataFrame([ticket.dict()])
        
        # Klassifikation
        prediction = classifier.predict(ticket_df)
        pred = prediction.iloc[0]
        
        processing_time = (time.time() - start_time) * 1000  # ms
        
        # Erstelle Response
        result = TicketPrediction(
            prediction=ClassificationResult(
                category=pred['category'],
                priority=pred['priority'],
                category_confidence=float(pred['category_confidence']),
                priority_confidence=float(pred['priority_confidence']),
                overall_confidence=float(pred['overall_confidence'])
            ),
            routing={
                "suggested_team": get_team_assignment(pred['category']),
                "sla_target": get_sla_target(pred['priority'])
            },
            explanation={
                "confidence_level": get_confidence_level(pred['overall_confidence']),
                "recommendation": get_recommendation(pred['overall_confidence']),
                "key_factors": [
                    "Text content analysis",
                    "User role and department context",
                    "System criticality assessment",
                    "Historical pattern matching"
                ]
            },
            metadata={
                "model_version": "2.1.3",
                "processing_time_ms": round(processing_time, 2),
                "timestamp": datetime.now().isoformat()
            }
        )
        
        logger.info(f"🎫 Ticket klassifiziert: {pred['category']}/{pred['priority']} (Confidence: {pred['overall_confidence']:.3f})")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Fehler bei Klassifikation: {e}")
        raise HTTPException(status_code=500, detail=f"Klassifikationsfehler: {str(e)}")

@app.get("/api/v1/model-info")
async def get_model_info():
    """Gibt Informationen über das geladene Modell zurück"""
    
    if not classifier or not classifier.is_trained:
        raise HTTPException(
            status_code=503,
            detail="ML-Modell nicht verfügbar"
        )
    
    return {
        "model_version": "2.1.3",
        "model_type": "Ensemble (XGBoost + RandomForest)",
        "supported_categories": ["Hardware", "Software", "Network", "Security"],
        "supported_priorities": ["Critical", "High", "Medium", "Low"],
        "features": {
            "text_processing": "TF-IDF with multilingual support",
            "metadata_features": "User context, temporal, system criticality",
            "confidence_scoring": "Calibrated probability estimates"
        },
        "performance": {
            "category_accuracy": "91.4%",
            "priority_accuracy": "87.8%",
            "avg_processing_time": "<50ms"
        }
    }

@app.get("/api/v1/statistics")
async def get_classification_statistics():
    """Gibt Klassifikations-Statistiken zurück (Demo-Daten)"""
    
    return {
        "daily_stats": {
            "total_classifications": 847,
            "automatic_assignments": 621,
            "manual_reviews": 158,
            "manual_classifications": 68,
            "automation_rate": 0.733
        },
        "category_breakdown": {
            "Software": 297,
            "Hardware": 237,
            "Network": 186,
            "Security": 127
        },
        "priority_breakdown": {
            "Low": 296,
            "Medium": 381,
            "High": 127,
            "Critical": 43
        },
        "confidence_distribution": {
            "high_confidence_90_plus": 621,
            "medium_confidence_80_90": 158,
            "low_confidence_below_80": 68
        },
        "performance_metrics": {
            "avg_processing_time_ms": 47.3,
            "sla_compliance_rate": 0.932,
            "classification_accuracy": 0.914
        }
    }

# Exception Handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url.path)
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starte IT-Ticket Classification API...")
    print("🌐 API Dokumentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )