QERCAS: Quantum-Enhanced Regulatory Compliance Alert System
QERCAS is a full-stack, AI-powered RegTech (Regulatory Technology) prototype for the investment banking sector. This system is designed to proactively detect and prevent financial compliance breaches by integrating a suite of next-generation technologies, including Explainable AI, Graph Neural Networks, and Post-Quantum Cryptography.

The platform provides a real-time dashboard for compliance officers to monitor live transactions, investigate high-risk alerts with AI-generated explanations, analyze suspicious networks, and query regulatory documents using natural language.

Live Dashboard
(Action Required: Replace this line with a screenshot of your running application. Drag and drop the image into your GitHub README.md editor.)

Core Features
Real-Time AI Analysis: A machine learning pipeline using Python (Scikit-learn/PyTorch) and asynchronous task queues (Celery, Redis) analyzes transactions in real-time, flagging them as Compliant, High-Risk, or Blocked.

Explainable AI (XAI): Integrates a SHAP (SHapley Additive exPlanations) engine to provide transparent, human-readable justifications for every AI-driven decision, ensuring model auditability and trust.

Graph Neural Network (GNN) Analysis: A GNN service (using NetworkX) dynamically builds and visualizes transaction networks to uncover sophisticated financial crime patterns like money laundering rings.

Natural Language Processing (NLP): An AI-powered regulatory search engine using a Hugging Face Transformers model allows officers to ask complex questions in plain English and receive precise answers.

Advanced Privacy & Security Modules: The architecture includes services for future-proof security:

Federated Learning: A simulated environment for training the core AI model across multiple institutions without sharing sensitive, private data.

Post-Quantum Cryptography (PQC): An integrated service using the Kyber algorithm to provide quantum-resistant encryption for critical data, protecting it from "Harvest Now, Decrypt Later" attacks.

Tech Stack
Area

Technology / Library

Frontend

React (Vite), Axios, Chart.js, Tailwind CSS

Backend

Django, Django REST Framework

AI / ML

Scikit-learn, PyTorch, SHAP, NetworkX, Transformers (Hugging Face)

Async Tasks

Celery, Redis

Database

SQLite (Development), PostgreSQL (Production-ready)

Security

py-oqs (Open Quantum Safe), pycryptodome (AES Fallback)

Local Setup and Installation
Follow these steps to run the project on your local machine.

Prerequisites
Python (3.10+) & Pip

Node.js & npm

Git

Redis

1. Clone the Repository
git clone [https://github.com/your-username/qercas-project.git](https://github.com/your-username/qercas-project.git)
cd qercas-project

2. Backend Setup
# Navigate to the backend directory
cd backend/qercas_project

# Create and activate a virtual environment
python -m venv ../venv
source ../venv/Scripts/activate

# Install Python dependencies
pip install -r ../requirements.txt

# Set up the database
python manage.py migrate

# Create an admin user for the Django admin panel
python manage.py createsuperuser

3. Frontend Setup
# Navigate to the frontend directory
cd ../../frontend

# Install JavaScript dependencies
npm install

4. Running the Full System
To run the application, you need to have four separate terminals open and running simultaneously.

Terminal 1 (Redis):

redis-server

Terminal 2 (Celery Worker):

# Navigate to backend/qercas_project and activate venv
celery -A qercas_project worker -l info

Terminal 3 (Django Backend):

# Navigate to backend/qercas_project and activate venv
python manage.py runserver

Terminal 4 (React Frontend):

# Navigate to frontend
npm run dev

Once all services are running, open your browser and navigate to the URL provided by the Vite server (usually http://localhost:5173).

Usage
Generate Live Data: To see the dashboard populate with data, run the stream simulator in a fifth terminal.

# Navigate to backend/qercas_project and activate venv
python stream_simulator.py
