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

const SummaryCards = () => (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card title="Real-Time Alerts" value={12} color="text-red-500" />
        <Card title="Pending Explanations" value={4} color="text-yellow-500" />
        <Card title="Active Quantum Tasks" value={2} color="text-blue-500" />
        <Card title="Regulatory Updates (24h)" value={7} color="text-gray-500" />
    </div>
);

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
                const newLabels = [...prevData.labels.slice(1), new Date().toLocaleTimeString()];
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
                            <td className="p-3 text-sm">{tx.transaction_type}</td>
                            <td className="p-3 text-sm font-semibold">${parseFloat(tx.amount).toFixed(2)}</td>
                            <td className="p-3 text-sm">{tx.client_name}</td>
                            <td className="p-3 text-sm"><StatusBadge status={tx.status} /></td>
                            <td className="p-3 text-sm">
                                <button onClick={() => onRowClick(tx)} className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600">
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

const DetailsModal = ({ transaction, explanation, onClose }) => {
    if (!transaction) return null;

    const isExplanationValid = explanation && !explanation.error && Array.isArray(explanation.shap_values);
    
    // --- FINAL CHANGE: This is the new URL for the GNN graph image ---
    const gnnGraphUrl = `http://127.0.0.1:8000/gnn/graph/${transaction.id}/`;

    // Safe calculation with error handling
    const calculateOutputValue = () => {
        try {
            if (!isExplanationValid) return "N/A";
            const baseValue = parseFloat(explanation.base_value) || 0;
            const shapSum = explanation.shap_values.reduce((a, b) => (parseFloat(a) || 0) + (parseFloat(b) || 0), 0);
            return (baseValue + shapSum).toFixed(2);
        } catch (error) {
            console.error("Error calculating output value:", error);
            return "Error";
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
                            {`ID:        ${transaction.transaction_id_str}\nTimestamp: ${new Date(transaction.timestamp).toLocaleString()}\nAmount:    $${parseFloat(transaction.amount).toFixed(2)}\nClient:    ${transaction.client_name}\nType:      ${transaction.transaction_type}`}
                        </pre>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                        <h4 className="font-bold mb-2">GNN Network Analysis</h4>
                        {/* --- FINAL CHANGE: Use the dynamic URL --- */}
                        <img 
                            src={gnnGraphUrl} 
                            alt="GNN Network Graph" 
                            className="rounded-md w-full"
                            onError={(e) => {
                                e.target.style.display = 'none';
                                e.target.nextSibling.textContent = 'Graph not available for this transaction.';
                            }}
                        />
                        <p className="text-sm mt-2">Network analysis visualization.</p>
                    </div>
                    <div className="md:col-span-2 bg-gray-50 p-4 rounded-lg">
                        <h4 className="font-bold mb-2">XAI Explanation (SHAP Force Plot)</h4>
                        {isExplanationValid ? (
                            <div className="font-mono text-xs">
                                <div className="text-center mb-2">
                                    <span className="text-gray-600">output value</span><br />
                                    <span className="text-2xl font-bold text-red-500">
                                        {calculateOutputValue()}
                                    </span>
                                </div>
                                <div className="flex items-center bg-gray-200 h-8 rounded w-full">
                                    {explanation.shap_values.map((val, i) => (
                                        <div key={i} className={`h-full ${val > 0 ? 'bg-red-500' : 'bg-blue-500'}`} style={{ width: `${Math.abs(val) * 100}%` }}></div>
                                    ))}
                                </div>
                                <div className="flex justify-between mt-2 text-gray-600">
                                    <span>Lower Risk ‹──</span>
                                    <span>──› Higher Risk</span>
                                </div>
                                <div className="flex justify-around mt-2 text-center">
                                    {explanation.feature_names.map((name, i) => (
                                        <div key={name}>
                                            <span className={`font-bold ${explanation.shap_values[i] > 0 ? 'text-red-500' : 'text-blue-500'}`}>
                                                {(parseFloat(explanation.shap_values[i]) || 0).toFixed(2)}
                                            </span><br/>
                                            <span className="text-gray-600">{name.replace('_', ' ')} = {explanation.feature_values[i]}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ) : (
                            <div className="text-center py-4 text-gray-500">
                                <p>No explanation available for this transaction.</p>
                                <p className="text-sm">Explanations are only generated for high-risk transactions.</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default function App() {
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

    return (
        <div className="bg-gray-100 min-h-screen p-8 font-sans">
            <div className="container mx-auto">
                <Header />
                <SummaryCards />
                <Charts />
                <div className="bg-white p-6 rounded-lg shadow-md">
                    <TransactionTable onRowClick={handleRowClick} />
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
