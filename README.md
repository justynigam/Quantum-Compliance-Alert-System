QERCAS: Quantum-Enhanced Regulatory Compliance Alert System
(Replace the URL above with a link to a screenshot of your final dashboard)

QERCAS is a full-stack proof-of-concept RegTech platform designed for modern investment banking. It leverages a suite of advanced technologies—including Explainable AI, Graph Neural Networks, and Quantum Computing—to proactively detect financial crime, ensure compliance, and provide long-term data security against future threats.

This project demonstrates a modular, scalable architecture for building next-generation financial monitoring systems.

🎥 Video Demo
A brief video walkthrough of the QERCAS dashboard, demonstrating the live transaction feed, the AI-powered risk analysis, the XAI explanation modal, the GNN graph visualization, and the NLP regulatory search in action.

Watch the full video demo here


https://github.com/user-attachments/assets/c5ba4181-7150-4e05-83f6-c93078c8020b

Core Features
This system is built as a collection of specialized services, each handling a critical compliance function:

Real-Time Transaction Monitoring: A live feed of transactions, powered by a React frontend and a Django REST API backend.

AI-Powered Risk Scoring: An asynchronous Celery task queue processes new transactions, using a machine learning model to assign a risk status (COMPLIANT, HIGH_RISK, BLOCKED).

Explainable AI (XAI) Engine: For any transaction flagged as high-risk, a SHAP (SHapley Additive exPlanations) force plot is generated and displayed, providing a transparent and auditable reason for the AI's decision.

Graph Neural Network (GNN) Analysis: Risky transactions automatically trigger a GNN service that maps out the network of related accounts, generating a graph visualization to help analysts spot complex fraud patterns.

NLP-Powered Regulatory Search: A user-friendly search interface that uses a pre-trained Transformer model (from Hugging Face) to answer natural language questions based on a corpus of regulatory documents.

Quantum-Resistant Cryptography (PQC): Protects sensitive customer and transaction data from "Harvest Now, Decrypt Later" attacks by future quantum computers. The architecture is designed to integrate a PQC library like liboqs for encrypting critical data fields.

Privacy-Preserving Verification (ZKP): The system design includes Zero-Knowledge Proof modules. This allows the system to prove to a regulator that a set of transactions is compliant without revealing any of the actual, sensitive transaction details.

Federated Learning for Model Training: The AI risk model is designed to be trained using a federated learning approach. This allows collaborative model improvement across different institutions without sharing any private data, simulated using a library like PySyft.

Quantum Machine Learning for Fraud Detection: The architecture includes a "Quantum Oracle" service. For certain high-complexity scenarios, it offloads analysis to a quantum algorithm using Qiskit to spot patterns that classical models might miss.

Technology Stack
The project is architected with a clean separation between the frontend, backend, and machine learning services.

Component

Technology

Frontend

axios, react-chartjs-2

Backend

Django REST Framework, django-cors-headers

ML & Async

Scikit-learn, SHAP, NetworkX, Matplotlib, Hugging Face Transformers, PyTorch, Qiskit

Database

SQLite (for development)

Setup and Installation
Follow these steps to get the project running on your local machine.

Prerequisites
Python (3.10+)

Node.js and npm

Redis

1. Backend Setup
First, set up the Django backend and all its services.

# 1. Navigate to the backend project directory
cd backend/qercas_project

# 2. Create and activate a Python virtual environment
python -m venv ../venv
source ../venv/Scripts/activate

# 3. Install all required Python packages
pip install -r ../requirements.txt

# 4. Set up the database
python manage.py makemigrations
python manage.py migrate

# 5. Create an admin user for the Django admin panel
python manage.py createsuperuser

# 6. Train the initial AI model
python ml_training/train_model.py

# 7. Seed the database with sample data
python manage.py seed

2. Frontend Setup
Next, set up the React frontend.

# 1. From the project root, navigate to the frontend directory
cd frontend

# 2. Install all required npm packages
npm install

Running the Application
To run the full application, you will need four separate terminals running at the same time.

Terminal 1: Start Redis
Redis acts as the message broker for our asynchronous tasks.

redis-server

Terminal 2: Start the Celery Worker
This is the "brain" that runs the AI and GNN analysis in the background.

# Navigate to backend/qercas_project and activate the venv
celery -A qercas_project worker -l info

Terminal 3: Start the Django Backend Server
This runs the API that your frontend will talk to.

# Navigate to backend/qercas_project and activate the venv
python manage.py runserver

Terminal 4: Start the React Frontend Server
This runs the user interface.

# Navigate to the frontend directory
npm run dev

You can now open your browser to the address shown in the Vite terminal (usually http://localhost:5173) to see the QERCAS dashboard in action!
