import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  ArcElement,
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler, ArcElement
);

// --- Reusable UI Components ---

const Card = ({ title, value, color }) => (
  <div className="bg-white p-6 rounded-lg shadow-md text-center">
    <h3 className="text-md font-semibold text-gray-500 mb-2">{title}</h3>
    <div className={`text-5xl font-bold ${color}`}>{value}</div>
  </div>
);

const StatusBadge = ({ status }) => {
  const statusStyles = {
    BLOCKED: 'bg-red-500 text-white',
    HIGH_RISK: 'bg-yellow-400 text-black',
    COMPLIANT: 'bg-green-500 text-white',
    PENDING: 'bg-gray-400 text-black',
  };
  const displayName = status.replace('_', ' ');
  return (
    <span className={`px-3 py-1 text-sm font-bold rounded-full capitalize ${statusStyles[status]}`}>
      {displayName}
    </span>
  );
};

// --- Main Dashboard Components ---

const Header = () => (
    <header className="mb-8">
        <h1 className="text-4xl font-bold text-blue-600">QERCAS Dashboard</h1>
        <p className="text-gray-600">Quantum-Enhanced Regulatory Compliance Alert System</p>
    </header>
);

const SummaryCards = () => {
    // Use state to hold the dynamic data, with initial loading values
    const [summaryData, setSummaryData] = useState({
        real_time_alerts: '...',
        pending_explanations: '...',
        active_quantum_tasks: '...',
        regulatory_updates: '...'
    });

    // Use useEffect to fetch the data when the component loads
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/summary/')
            .then(response => {
                setSummaryData(response.data);
            })
            .catch(error => {
                console.error("Error fetching summary data:", error);
                setSummaryData({
                    real_time_alerts: 'N/A',
                    pending_explanations: 'N/A',
                    active_quantum_tasks: 'N/A',
                    regulatory_updates: 'N/A'
                });
            });
    }, []); // Empty array means this runs only once on mount

    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <Card title="Real-Time Alerts" value={summaryData.real_time_alerts} color="text-red-500" />
            <Card title="Pending Explanations" value={summaryData.pending_explanations} color="text-yellow-500" />
            <Card title="Active Quantum Tasks" value={summaryData.active_quantum_tasks} color="text-blue-500" />
            <Card title="Regulatory Updates (24h)" value={summaryData.regulatory_updates} color="text-gray-500" />
        </div>
    );
};

const Charts = () => {
    const [lineData, setLineData] = useState({
        labels: ['-15s', '-12.5s', '-10s', '-7.5s', '-5s', '-2.5s', 'Now'],
        datasets: [{
            label: 'Alerts',
            data: [5, 8, 4, 7, 10, 6, 12],
            borderColor: 'rgba(220, 53, 69, 1)',
            backgroundColor: 'rgba(220, 53, 69, 0.1)',
            fill: true,
            tension: 0.4
        }]
    });

    useEffect(() => {
        const interval = setInterval(() => {
            setLineData(prevData => {
                const newLabels = [...prevData.labels.slice(1), new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })];
                const newData = [...prevData.datasets[0].data.slice(1), Math.floor(Math.random() * 15) + 1];
                return { ...prevData, labels: newLabels, datasets: [{ ...prevData.datasets[0], data: newData }] };
            });
        }, 2500);
        return () => clearInterval(interval);
    }, []);

    const doughnutData = {
        labels: ['AML/CFT', 'Market Abuse', 'Internal Fraud', 'Suitability'],
        datasets: [{ data: [45, 25, 15, 15], backgroundColor: ['#dc3545', '#ffc107', '#0d6efd', '#6c757d'] }]
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="font-bold mb-4">Alerts Over Time (Live)</h3>
                <Line data={lineData} options={{ responsive: true }} />
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="font-bold mb-4">Alerts by Risk Category</h3>
                <Doughnut data={doughnutData} options={{ responsive: true }} />
            </div>
        </div>
    );
};

const TransactionTable = ({ onRowClick }) => {
    const [transactions, setTransactions] = useState([]);
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/transactions/')
            .then(response => setTransactions(response.data))
            .catch(error => console.error("Error fetching transactions:", error));
    }, []);

    return (
        <div className="overflow-x-auto">
            <table className="min-w-full bg-white">
                <thead className="bg-gray-100">
                    <tr>
                        {['ID', 'Timestamp', 'Type', 'Amount', 'Client', 'Status', 'Action'].map(head => (
                            <th key={head} className="p-3 text-left text-sm font-semibold text-gray-600">{head}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {transactions.map((tx) => (
                        <tr key={tx.id} className="border-b hover:bg-gray-50">
                            <td className="p-3 text-sm font-mono">{tx.transaction_id_str}</td>
                            <td className="p-3 text-sm">{new Date(tx.timestamp).toLocaleString()}</td>
                            <td className="p-3 text-sm">{tx.transaction_type.replace('_', ' ')}</td>
                            <td className="p-3 text-sm font-semibold">${parseFloat(tx.amount).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                            <td className="p-3 text-sm">{tx.client_name}</td>
                            <td className="p-3 text-sm"><StatusBadge status={tx.status} /></td>
                            <td className="p-3 text-sm">
                                <button onClick={() => onRowClick(tx)} className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 transition-colors">
                                    View Details
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

const RegulatorySearch = () => {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSearch = async () => {
        if (!question.trim()) return;
        setIsLoading(true);
        setAnswer('');
        try {
            const response = await axios.post('http://127.0.0.1:8000/nlp/search/', { question });
            setAnswer(response.data.answer);
        } catch (error) {
            console.error("Error fetching answer:", error);
            setAnswer("Sorry, I couldn't fetch an answer at this time.");
        }
        setIsLoading(false);
    };

    return (
        <div>
            <div className="flex space-x-2">
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask a question, e.g., 'What is the transaction limit in the EU?'"
                    className="flex-grow p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none transition-shadow"
                    onKeyUp={(e) => e.key === 'Enter' && handleSearch()}
                />
                <button 
                    onClick={handleSearch} 
                    disabled={isLoading}
                    className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:bg-blue-300 transition-colors"
                >
                    {isLoading ? 'Searching...' : 'Search'}
                </button>
            </div>
            {answer && (
                <div className="mt-4 p-4 bg-gray-100 rounded-lg animate-fade-in">
                    <p className="font-bold text-gray-800">Answer:</p>
                    <p className="text-gray-700">{answer}</p>
                </div>
            )}
        </div>
    );
};


const DetailsModal = ({ transaction, explanation, onClose }) => {
    if (!transaction) return null;

    const isExplanationValid = explanation && !explanation.error && Array.isArray(explanation.shap_values);
    const gnnGraphUrl = `http://127.0.0.1:8000/gnn/graph/${transaction.id}/`;
    
    // Safe calculation of output value
    const calculateOutputValue = () => {
        if (!isExplanationValid) return 0;
        try {
            const baseValue = parseFloat(explanation.base_value) || 0;
            const shapSum = explanation.shap_values.reduce((sum, val) => sum + (parseFloat(val) || 0), 0);
            return baseValue + shapSum;
        } catch (error) {
            console.error("Error calculating output value:", error);
            return 0;
        }
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-center items-center p-4">
            <div className="bg-white rounded-lg shadow-2xl w-full max-w-4xl max-h-full overflow-y-auto">
                <div className="p-6 border-b flex justify-between items-center">
                    <h2 className="text-2xl font-bold">Analysis for {transaction.transaction_id_str}</h2>
                    <button onClick={onClose} className="text-gray-500 hover:text-gray-800 text-3xl">&times;</button>
                </div>
                <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-gray-50 p-4 rounded-lg">
                        <h4 className="font-bold mb-2">Transaction Information</h4>
                        <pre className="text-sm whitespace-pre-wrap font-mono">
                            {`ID:        ${transaction.transaction_id_str}\nTimestamp: ${new Date(transaction.timestamp).toLocaleString()}\nAmount:    $${parseFloat(transaction.amount).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}\nClient:    ${transaction.client_name}\nType:      ${transaction.transaction_type.replace('_', ' ')}`}
                        </pre>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                        <h4 className="font-bold mb-2">GNN Network Analysis</h4>
                        <img src={gnnGraphUrl} alt="GNN Network Graph" className="rounded-md w-full" />
                        <p className="text-sm mt-2">Network analysis visualization.</p>
                    </div>
                    <div className="md:col-span-2 bg-gray-50 p-4 rounded-lg">
                        <h4 className="font-bold mb-2">XAI Explanation (SHAP Force Plot)</h4>
                        {isExplanationValid ? (
                            <div className="font-mono text-xs">
                                <div className="text-center mb-2">
                                    <span className="text-gray-600">output value</span><br />
                                    <span className="text-2xl font-bold text-red-500">
                                        {calculateOutputValue().toFixed(2)}
                                    </span>
                                </div>
                                <div className="flex items-center bg-gray-200 h-8 rounded w-full">
                                    {explanation.shap_values.map((val, i) => {
                                        const numVal = parseFloat(val) || 0;
                                        return (
                                            <div key={i} className={`h-full ${numVal > 0 ? 'bg-red-500' : 'bg-blue-500'}`} style={{ width: `${Math.abs(numVal) * 100}%` }}></div>
                                        );
                                    })}
                                </div>
                                <div className="flex justify-between mt-2 text-gray-600">
                                    <span>Lower Risk ‹──</span>
                                    <span>──› Higher Risk</span>
                                </div>
                                <div className="flex justify-around mt-2 text-center">
                                    {explanation.feature_names && explanation.feature_names.map((name, i) => {
                                        const shapValue = parseFloat(explanation.shap_values[i]) || 0;
                                        return (
                                            <div key={name}>
                                                <span className={`font-bold ${shapValue > 0 ? 'text-red-500' : 'text-blue-500'}`}>
                                                    {shapValue.toFixed(2)}
                                                </span><br/>
                                                <span className="text-gray-600">{name.replace('_', ' ')} = {explanation.feature_values && explanation.feature_values[i]}</span>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        ) : <p className="text-center py-4 text-gray-500">Loading explanation or not applicable...</p>}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default function App() {
    const [activeTab, setActiveTab] = useState('transactions');
    const [selectedTx, setSelectedTx] = useState(null);
    const [explanation, setExplanation] = useState(null);

    const handleRowClick = (tx) => {
        setSelectedTx(tx);
        setExplanation(null); // Clear previous explanation

        if (tx.status === 'HIGH_RISK' || tx.status === 'BLOCKED') {
            axios.get(`http://127.0.0.1:8000/api/transactions/${tx.id}/explanation/`)
                .then(response => {
                    setExplanation(response.data);
                })
                .catch(error => {
                    console.error("Error fetching explanation:", error);
                    setExplanation({ error: "Explanation not available." });
                });
        }
    };
    
    // Helper to render the correct content for the active tab
    const renderTabContent = () => {
        switch (activeTab) {
            case 'search':
                return <RegulatorySearch />;
            case 'transactions':
            default:
                return <TransactionTable onRowClick={handleRowClick} />;
        }
    };

    return (
        <div className="bg-gray-100 min-h-screen p-8 font-sans">
            <div className="container mx-auto">
                <Header />
                <SummaryCards />
                <Charts />
                <div className="bg-white p-6 rounded-lg shadow-md">
                    {/* --- TABS --- */}
                    <div className="border-b mb-4">
                        <nav className="flex space-x-4">
                            <button 
                                onClick={() => setActiveTab('transactions')}
                                className={`py-2 px-4 font-semibold transition-colors ${activeTab === 'transactions' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-blue-600'}`}
                            >
                                Transaction Feed
                            </button>
                            <button 
                                onClick={() => setActiveTab('search')}
                                className={`py-2 px-4 font-semibold transition-colors ${activeTab === 'search' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-blue-600'}`}
                            >
                                Regulatory Search
                            </button>
                        </nav>
                    </div>
                    {/* --- RENDER ACTIVE TAB CONTENT --- */}
                    {renderTabContent()}
                </div>
            </div>
            <DetailsModal 
                transaction={selectedTx} 
                explanation={explanation}
                onClose={() => setSelectedTx(null)} 
            />
        </div>
    );
}