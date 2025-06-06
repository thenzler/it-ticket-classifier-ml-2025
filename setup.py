#!/usr/bin/env python3
"""
Setup Script für IT-Ticket Classification System

ATL - HF Wirtschaftsinformatik
Autor: Benjamin Peter
Datum: 08.06.2025
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="it-ticket-classifier",
    version="2.1.3",
    author="Benjamin Peter",
    author_email="benjamin.peter@student.hf-ict.ch",
    description="Machine Learning System für automatische IT-Ticket Klassifizierung",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thenzler/it-ticket-classifier-ml-2025",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
        "api": [
            "fastapi>=0.68.0",
            "uvicorn[standard]>=0.15.0",
        ],
        "viz": [
            "matplotlib>=3.4.0",
            "seaborn>=0.11.0",
            "plotly>=5.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "it-ticket-train=models.train_classifier:main",
            "it-ticket-api=api.main:main",
            "it-ticket-generate-data=data.generate_sample_data:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.yml", "*.yaml"],
    },
    keywords="machine-learning nlp it-support ticket-classification xgboost",
    project_urls={
        "Bug Reports": "https://github.com/thenzler/it-ticket-classifier-ml-2025/issues",
        "Source": "https://github.com/thenzler/it-ticket-classifier-ml-2025",
        "Documentation": "https://github.com/thenzler/it-ticket-classifier-ml-2025/wiki",
    },
)