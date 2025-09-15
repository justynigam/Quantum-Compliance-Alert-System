# QERCAS - Quantum-Enhanced Regulatory Compliance Alert System

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-19.1-blue.svg)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://python.org/)

A cutting-edge financial compliance monitoring system that leverages quantum-resistant cryptography, advanced machine learning, and real-time analytics to detect and prevent financial crimes while ensuring regulatory compliance.

## 🌟 Key Features

### 🔐 Quantum-Resistant Security
- **Post-Quantum Cryptography**: Implementation using liboqs with Kyber768 algorithm
- **Fallback Encryption**: AES-256 encryption when quantum libraries are unavailable
- **Privacy Vault**: Secure storage and processing of sensitive financial data

### 🤖 Advanced AI/ML Analytics
- **Graph Neural Networks (GNN)**: Network analysis for detecting suspicious transaction patterns
- **Natural Language Processing**: Regulatory document search and compliance queries
- **Explainable AI (XAI)**: SHAP-based explanations for risk decisions
- **Federated Learning**: Distributed machine learning for privacy-preserving model training

### 📊 Real-Time Monitoring
- **Live Transaction Feed**: Real-time processing and risk assessment
- **Interactive Dashboard**: Modern React-based interface with live charts
- **Alert Management**: Automated risk categorization and compliance alerts
- **Network Visualization**: Dynamic graph visualizations of transaction networks

### 🏦 Regulatory Compliance
- **Multi-Risk Categories**: AML/CFT, Market Abuse, Internal Fraud, Suitability checks
- **Automated Reporting**: Compliance reports and regulatory notifications
- **Audit Trail**: Complete transaction history with cryptographic integrity

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend│    │   Django API     │    │   ML Services   │
│   (Dashboard)   │◄──►│   (REST API)     │◄──►│   (Analysis)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                       ┌────────▼────────┐    ┌─────────▼─────────┐
                       │   PostgreSQL    │    │   Redis/Celery    │
                       │   (Database)    │    │   (Task Queue)    │
                       └─────────────────┘    └───────────────────┘
```

### Core Components

- **Frontend**: React 19.1 + Vite + TailwindCSS + Chart.js
- **Backend**: Django 5.2 + Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **Task Queue**: Celery + Redis for asynchronous processing
- **ML Libraries**: PyTorch, scikit-learn, NetworkX, SHAP
- **Quantum Security**: liboqs-python, PyCryptodome

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Redis server
- Git

**Optional for Enhanced Security:**
- liboqs library for quantum-resistant cryptography
- CMake and Visual Studio Build Tools (Windows)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/justynigam/Quantum-Compliance-Alert-System.git
   cd Quantum-Compliance-Alert-System
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   cd qercas_project
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic
   ```

3. **Frontend Setup**
   ```bash
   cd frontend/frontend
   npm install
   ```

4. **Start Redis Server**
   ```bash
   redis-server
   ```

### Configuration

Create a `.env` file in `backend/qercas_project/` for environment-specific settings:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Optional - defaults to SQLite)
DATABASE_URL=postgresql://user:password@localhost:5432/qercas

# Celery/Redis
CELERY_BROKER_URL=redis://localhost:6379/0
REDIS_URL=redis://localhost:6379

# ML Model Settings
ML_MODEL_PATH=./ml_models/
ENABLE_QUANTUM_CRYPTO=True

# API Settings
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Troubleshooting Installation

**Quantum Cryptography Issues:**
If liboqs-python installation fails, the system will automatically fall back to AES-256 encryption:
```bash
# Test quantum crypto availability
cd backend/qercas_project
python test_oqs.py
```

**Windows-Specific Issues:**
- Install Visual Studio Build Tools for C++ compilation
- Use Windows Subsystem for Linux (WSL) for better compatibility
- Redis: Use Redis for Windows or run via Docker

### Running the Application

1. **Start the Backend**
   ```bash
   cd backend/qercas_project
   python manage.py runserver
   ```

2. **Start Celery Worker** (new terminal)
   
   **Linux/macOS:**
   ```bash
   cd backend/qercas_project
   celery -A qercas_project worker --loglevel=info
   ```
   
   **Windows:**
   ```bash
   cd backend
   run_celery.bat
   ```

3. **Start Frontend** (new terminal)
   ```bash
   cd frontend/frontend
   npm run dev
   ```

4. **Access the Application**
   - Frontend Dashboard: http://localhost:5173
   - Backend API: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

## 📊 Usage

### Dashboard Overview

The main dashboard provides:
- **Real-time Alerts**: Live monitoring of high-risk transactions
- **Summary Cards**: Key metrics including active alerts and pending explanations
- **Interactive Charts**: Time-series analysis and risk category distribution
- **Transaction Feed**: Searchable list of all transactions with status indicators

### Transaction Analysis

1. **Automatic Risk Assessment**: Every transaction is automatically analyzed using ML models
2. **Risk Categories**: 
   - `COMPLIANT`: Low-risk, approved transactions
   - `HIGH_RISK`: Requires human review
   - `BLOCKED`: Automatically rejected due to high risk
   - `PENDING`: Under analysis

3. **Explainable AI**: Click "View Details" on high-risk transactions to see:
   - SHAP force plots explaining risk factors
   - Network graph visualizations
   - Feature importance analysis

### Regulatory Search

Use the NLP-powered search to query regulatory requirements:
- "What is the transaction limit in the EU?"
- "AML requirements for crypto transactions"
- "KYC documentation needed for wire transfers"

## 🔌 API Documentation

### Core Endpoints

#### Transactions
- `GET /api/transactions/` - List all transactions
- `POST /api/transactions/` - Create new transaction
- `GET /api/transactions/{id}/` - Get specific transaction
- `GET /api/transactions/{id}/explanation/` - Get XAI explanation

#### Analytics
- `GET /api/summary/` - Dashboard summary statistics
- `GET /gnn/graph/{id}/` - Generate network graph for transaction
- `POST /nlp/search/` - Query regulatory knowledge base

### Example Transaction Creation

```python
import requests

transaction_data = {
    "transaction_id_str": "TXN001",
    "transaction_type": "WIRE",
    "amount": "50000.00",
    "currency": "USD",
    "client_name": "John Doe",
    "source_account": "ACC123",
    "destination_account": "ACC456"
}

response = requests.post(
    "http://localhost:8000/api/transactions/",
    json=transaction_data
)
```

## 🛠️ Development

### Project Structure

```
Quantum-Compliance-Alert-System/
├── backend/
│   └── qercas_project/
│       ├── transactions/         # Core transaction models
│       ├── privacy_vault/        # Quantum cryptography
│       ├── gnn_analyzer/         # Graph neural networks
│       ├── nlp_processor/        # Natural language processing
│       ├── xai_engine/           # Explainable AI
│       ├── federated_learning/   # Distributed ML
│       └── ml_models/            # ML model storage
├── frontend/
│   └── frontend/
│       ├── src/
│       │   ├── App.jsx          # Main dashboard component
│       │   └── main.jsx         # React entry point
│       └── public/              # Static assets
└── README.md
```

### Key Technologies

- **Quantum Cryptography**: Post-quantum key encapsulation using Kyber768
- **Machine Learning**: PyTorch for deep learning, scikit-learn for traditional ML
- **Graph Analysis**: NetworkX for transaction network modeling
- **Explainability**: SHAP for model interpretability
- **Visualization**: Chart.js for real-time charts, custom network graphs

### Adding New Features

1. **New Transaction Types**: Update `Transaction.TransactionType` choices
2. **Additional ML Models**: Add models to `ml_models/` directory
3. **Custom Risk Rules**: Implement in `xai_engine/services.py`
4. **UI Components**: Add React components in `frontend/src/`

### Testing

```bash
# Backend tests
cd backend/qercas_project
python manage.py test

# Frontend tests (if available)
cd frontend/frontend
npm test
```

## 🔒 Security Features

### Quantum-Resistant Cryptography
- **Algorithm**: Kyber768 (NIST-selected post-quantum algorithm)
- **Key Management**: Secure key generation and storage
- **Fallback**: AES-256 when quantum libraries unavailable

### Data Protection
- **Encryption at Rest**: All sensitive data encrypted using PQC
- **Secure Transmission**: HTTPS/TLS for all API communications
- **Access Control**: Role-based permissions and authentication

### Compliance Standards
- **GDPR**: Privacy-by-design architecture
- **PCI DSS**: Secure payment data handling
- **SOX**: Comprehensive audit trails
- **BASEL III**: Risk management compliance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript
- Add tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/justynigam/Quantum-Compliance-Alert-System/issues)
- **Documentation**: Check the `/docs` directory (if available)
- **Contact**: Open an issue for questions or support requests

## 🚧 Roadmap

- [ ] Real-time model retraining
- [ ] Multi-language NLP support
- [ ] Advanced quantum algorithms integration
- [ ] Mobile dashboard application
- [ ] Blockchain integration for audit trails
- [ ] Advanced federated learning protocols

---

**Note**: This system is designed for educational and research purposes. For production deployment in regulated environments, ensure compliance with local financial regulations and conduct thorough security audits.