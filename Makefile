# Makefile für IT-Ticket Classification System
# ATL - HF Wirtschaftsinformatik
# Autor: Benjamin Peter
# Datum: 08.06.2025

.PHONY: help install install-dev setup clean test lint format train api docker-build docker-run data

# Default target
help:
	@echo "🎫 IT-Ticket Classification System - HF Wirtschaftsinformatik"
	@echo "=" 
	@echo "Verfügbare Commands:"
	@echo ""
	@echo "  📦 Setup & Installation:"
	@echo "    install      - Installiere Production Dependencies"
	@echo "    install-dev  - Installiere Development Dependencies"
	@echo "    setup        - Komplettes Setup (install + data + train)"
	@echo ""
	@echo "  📋 Data & Training:"
	@echo "    data         - Generiere Beispieldaten"
	@echo "    train        - Trainiere ML-Modell"
	@echo ""
	@echo "  🌐 API & Services:"
	@echo "    api          - Starte FastAPI Server"
	@echo "    api-dev      - Starte API im Development Mode"
	@echo ""
	@echo "  🐳 Docker:"
	@echo "    docker-build - Build Docker Image"
	@echo "    docker-run   - Run Docker Container"
	@echo "    docker-dev   - Run mit docker-compose"
	@echo ""
	@echo "  🧪 Testing & Quality:"
	@echo "    test         - Run Tests"
	@echo "    test-cov     - Run Tests mit Coverage"
	@echo "    lint         - Code Linting"
	@echo "    format       - Code Formatting"
	@echo ""
	@echo "  🧹 Cleanup:"
	@echo "    clean        - Cleanup temporäre Dateien"
	@echo "    clean-all    - Cleanup alles (inkl. Daten & Modelle)"

# Installation
install:
	@echo "📦 Installiere Production Dependencies..."
	pip install -r requirements.txt

install-dev: install
	@echo "🔧 Installiere Development Dependencies..."
	pip install -r requirements-dev.txt
	@echo "🔎 Installiere Pre-commit Hooks..."
	pre-commit install || echo "Pre-commit nicht verfügbar"

setup: install data train
	@echo "✅ Setup komplett!"

# Data Generation
data:
	@echo "📋 Generiere Beispieldaten..."
	python src/data/generate_sample_data.py

# Model Training
train:
	@echo "🤖 Trainiere ML-Modell..."
	python src/models/train_classifier.py

# API
api:
	@echo "🌐 Starte FastAPI Server..."
	cd src && python api/main.py

api-dev:
	@echo "🔄 Starte API im Development Mode..."
	cd src && uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Docker
docker-build:
	@echo "🐳 Build Docker Image..."
	docker build -t it-ticket-classifier:latest .

docker-run: docker-build
	@echo "🚀 Run Docker Container..."
	docker run -p 8000:8000 --name it-ticket-classifier it-ticket-classifier:latest

docker-dev:
	@echo "🔄 Starte mit docker-compose..."
	docker-compose up --build

docker-stop:
	@echo "🛑 Stoppe Docker Services..."
	docker-compose down

# Testing
test:
	@echo "🧪 Run Tests..."
	pytest tests/ -v

test-cov:
	@echo "📈 Run Tests mit Coverage..."
	pytest tests/ --cov=src --cov-report=html --cov-report=term

# Code Quality
lint:
	@echo "🔍 Code Linting..."
	flake8 src/ tests/
	@echo "🔎 Type Checking..."
	mypy src/ || echo "Type checking fehlgeschlagen"

format:
	@echo "✨ Code Formatting..."
	black src/ tests/
	@echo "🗺️ Import Sorting..."
	isort src/ tests/ || echo "isort nicht verfügbar"

# Cleanup
clean:
	@echo "🧹 Cleanup temporäre Dateien..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + || true
	find . -type f -name ".coverage" -delete || true
	find . -type d -name "htmlcov" -exec rm -rf {} + || true
	find . -type f -name "*.log" -delete || true

clean-all: clean
	@echo "⚠️  Cleanup ALLES (inkl. Daten & Modelle)..."
	rm -rf data/raw/*.csv || true
	rm -rf data/processed/*.csv || true
	rm -rf data/models/*.pkl || true
	rm -rf data/models/*.joblib || true
	@echo "✅ Cleanup komplett!"

# Development Helpers
notebook:
	@echo "📓 Starte Jupyter Notebook..."
	jupyter notebook notebooks/

profile:
	@echo "📈 Performance Profiling..."
	python -m cProfile -o profile.prof src/models/train_classifier.py
	@echo "Profile gespeichert in profile.prof"

# Documentation
docs:
	@echo "📖 Generiere Dokumentation..."
	mkdocs build || echo "MkDocs nicht verfügbar"

docs-serve:
	@echo "🌐 Starte Dokumentations-Server..."
	mkdocs serve || echo "MkDocs nicht verfügbar"

# Monitoring & Health
health:
	@echo "🔍 Health Check..."
	curl -f http://localhost:8000/health || echo "API nicht erreichbar"

stats:
	@echo "📈 API Statistiken..."
	curl -s http://localhost:8000/api/v1/statistics | python -m json.tool || echo "API nicht erreichbar"

# Deployment
deploy-prep:
	@echo "📦 Deployment Vorbereitung..."
	make clean
	make test
	make lint
	make docker-build
	@echo "✅ Ready für Deployment!"

# Project Info
info:
	@echo "📋 Projekt Informationen:"
	@echo "Name: IT-Ticket Classification System"
	@echo "Version: 2.1.3"
	@echo "Autor: Benjamin Peter"
	@echo "Schule: ATL - HF Wirtschaftsinformatik"
	@echo "Modul: Big Data & AI"
	@echo "Datum: 08.06.2025"
	@echo ""
	@echo "Repository: https://github.com/thenzler/it-ticket-classifier-ml-2025"
	@echo "Dokumentation: http://localhost:8000/docs (wenn API läuft)"