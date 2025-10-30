QERCAS: Quantum-Enhanced Regulatory Compliance Alert System
QERCAS is a full-stack, AI-powered RegTech (Regulatory Technology) prototype for the investment banking sector. This system is designed to proactively detect and prevent financial compliance breaches by integrating a suite of next-generation technologies, including Explainable AI, Graph Neural Networks, and Post-Quantum Cryptography.

The platform provides a real-time dashboard for compliance officers to monitor live transactions, investigate high-risk alerts with AI-generated explanations, analyze suspicious networks, and query regulatory documents using natural language.

# Live Dashboard

https://github.com/user-attachments/assets/dd7ece65-13c5-4fa9-a393-2e986d758eb6

**Core Features**
Real-Time AI Analysis: A machine learning pipeline using Python (Scikit-learn/PyTorch) and asynchronous task queues (Celery, Redis) analyzes transactions in real-time, flagging them as Compliant, High-Risk, or Blocked.

**Explainable AI (XAI)**: Integrates a SHAP (SHapley Additive exPlanations) engine to provide transparent, human-readable justifications for every AI-driven decision, ensuring model auditability and trust.

**Graph Neural Network (GNN) Analysis**: A GNN service (using NetworkX) dynamically builds and visualizes transaction networks to uncover sophisticated financial crime patterns like money laundering rings.

**Natural Language Processing (NLP)**: An AI-powered regulatory search engine using a Hugging Face Transformers model allows officers to ask complex questions in plain English and receive precise answers.

**Advanced Privacy & Security Modules**: The architecture includes services for future-proof security:

**Federated Learning**: A simulated environment for training the core AI model across multiple institutions without sharing sensitive, private data.

**Post-Quantum Cryptography (PQC)**: An integrated service using the Kyber algorithm to provide quantum-resistant encryption for critical data, protecting it from "Harvest Now, Decrypt Later" attacks.

## Stack

- Backend: Django (Python 3.11+), Celery
- Broker: Redis
- Frontend: React (Node.js 18+ / npm)
- Task scheduling: Celery Beat or `django_celery_beat`
- Dev tooling: Docker Desktop (for Redis), Git, PowerShell (Windows)

## Prerequisites

- Windows 10/11 with PowerShell
- Python 3.11+
- Node.js 18+ and npm
- Docker Desktop (for Redis)
- Git

## Quick Start (local, Windows / PowerShell)

### 1) Clone

git clone <your-repo-url>
cd <your-repo-root>
# go to backend
cd backend

# create & activate venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install dependencies
pip install -r requirements.txt
# if the file exists in your project, also run:
if (Test-Path ".\qercas_project\requirements.txt") { pip install -r .\qercas_project\requirements.txt }

#Database
- python manage.py migrate
- python manage.py createsuperuser

#Run Django Server
- python manage.py runserver
# visit http://127.0.0.1:8000


# Celery
cd backend
.\.venv\Scripts\Activate.ps1
# Celery worker (Windows may require -P solo)
celery -A qercas_project worker -l info -P solo

# Optional: Celery beat (for periodic tasks)
celery -A qercas_project beat -l info

# Frotend
- cd ..\frontend
- npm install
- npm run dev
- # visit http://localhost:3000





