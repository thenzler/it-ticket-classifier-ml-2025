#!/usr/bin/env python3
"""
Unit Tests für IT-Ticket Classification System

ATL - HF Wirtschaftsinformatik
Autor: Benjamin Peter
Datum: 08.06.2025
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.train_classifier import ITTicketClassifier

class TestITTicketClassifier:
    """Test Suite für ITTicketClassifier"""
    
    @pytest.fixture
    def sample_data(self):
        """Erstellt Beispiel-Daten für Tests"""
        return pd.DataFrame([
            {
                'title': 'Laptop won\'t start',
                'description': 'Black screen when pressing power button',
                'category': 'Hardware',
                'priority': 'High',
                'user_role': 'end_user',
                'department': 'Finance',
                'affected_system': 'workstation',
                'hour_submitted': 14,
                'is_weekend': 0,
                'previous_tickets_30d': 1
            },
            {
                'title': 'Email server down',
                'description': 'Cannot connect to email server timeout error',
                'category': 'Network',
                'priority': 'Critical',
                'user_role': 'admin',
                'department': 'IT',
                'affected_system': 'email',
                'hour_submitted': 8,
                'is_weekend': 0,
                'previous_tickets_30d': 15
            },
            {
                'title': 'Suspicious email received',
                'description': 'Phishing attempt asking for credentials',
                'category': 'Security',
                'priority': 'High',
                'user_role': 'manager',
                'department': 'HR',
                'affected_system': 'email',
                'hour_submitted': 16,
                'is_weekend': 0,
                'previous_tickets_30d': 0
            },
            {
                'title': 'Software crashes frequently',
                'description': 'Application keeps crashing when saving files',
                'category': 'Software',
                'priority': 'Medium',
                'user_role': 'end_user',
                'department': 'Operations',
                'affected_system': 'erp',
                'hour_submitted': 10,
                'is_weekend': 0,
                'previous_tickets_30d': 3
            }
        ])
    
    @pytest.fixture
    def classifier(self):
        """Erstellt Classifier-Instanz"""
        return ITTicketClassifier()
    
    def test_classifier_initialization(self, classifier):
        """Test Initialisierung des Classifiers"""
        assert classifier.category_model is None
        assert classifier.priority_model is None
        assert classifier.text_vectorizer is None
        assert classifier.is_trained is False
        assert isinstance(classifier.it_stopwords, set)
    
    def test_text_preprocessing(self, classifier):
        """Test Text-Preprocessing"""
        # Test normale Eingabe
        text = "My laptop won't start. Please help urgently!"
        processed = classifier.preprocess_text(text)
        assert isinstance(processed, str)
        assert len(processed) > 0
        
        # Test mit None/NaN
        assert classifier.preprocess_text(None) == ""
        assert classifier.preprocess_text(pd.NA) == ""
        
        # Test IT-spezifische Begriffe
        text = "PC wifi email error"
        processed = classifier.preprocess_text(text)
        assert "computer" in processed or "pc" in processed
    
    def test_feature_creation(self, classifier, sample_data):
        """Test Feature Engineering"""
        features_df = classifier.create_features(sample_data)
        
        # Prüfe ob alle erwarteten Features vorhanden sind
        expected_features = [
            'combined_text', 'processed_text', 'is_admin', 'is_developer',
            'is_offhours', 'is_frequent_user', 'is_new_user', 'is_critical_system',
            'text_length', 'word_count', 'has_urgent_keywords'
        ]
        
        for feature in expected_features:
            assert feature in features_df.columns
        
        # Prüfe Datentypen
        binary_features = ['is_admin', 'is_developer', 'is_offhours', 
                          'is_frequent_user', 'is_new_user', 'is_critical_system',
                          'has_urgent_keywords']
        
        for feature in binary_features:
            assert features_df[feature].dtype in [np.int64, int, bool]
            assert features_df[feature].isin([0, 1]).all()
    
    def test_encoding_setup(self, classifier, sample_data):
        """Test Setup der Label Encoder"""
        classifier.setup_encoders(sample_data)
        
        expected_encoders = ['user_role', 'department', 'affected_system']
        for encoder_name in expected_encoders:
            assert encoder_name in classifier.label_encoders
            assert hasattr(classifier.label_encoders[encoder_name], 'classes_')
    
    def test_prediction_without_training(self, classifier, sample_data):
        """Test Vorhersage ohne Training (sollte Fehler werfen)"""
        with pytest.raises(ValueError, match="Modell muss zuerst trainiert werden"):
            classifier.predict(sample_data)