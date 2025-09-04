import os
import networkx as nx
import matplotlib.pyplot as plt
from django.conf import settings
from transactions.models import Transaction
from django.db.models import Q # Make sure Q is imported

class GNNService:
    @staticmethod
    def analyze_and_generate_graph(transaction_id):
        """
        Finds related transactions and generates a network graph image.
        """
        try:
            # 1. Find the core transaction
            center_tx = Transaction.objects.get(id=transaction_id)
            
            # 2. Find related transactions
            related_txns = Transaction.objects.filter(
                Q(source_account=center_tx.source_account) |
                Q(destination_account=center_tx.destination_account)
            ).exclude(id=transaction_id).distinct()[:10] # Limit to 10 for readability

            # 3. Build the graph
            G = nx.Graph()
            accounts = {center_tx.source_account, center_tx.destination_account}
            for tx in related_txns:
                accounts.add(tx.source_account)
                accounts.add(tx.destination_account)
            
            for acc in accounts:
                G.add_node(acc)

            G.add_edge(center_tx.source_account, center_tx.destination_account)
            for tx in related_txns:
                G.add_edge(tx.source_account, tx.destination_account)

            # 4. Generate and save the graph image
            plt.figure(figsize=(10, 7))
            pos = nx.spring_layout(G)
            nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='gray', font_size=9)
            
            # --- THIS IS THE CORRECTED PATH LOGIC ---
            # It now correctly uses the MEDIA_ROOT from settings.py to build the path.
            graph_dir = os.path.join(settings.MEDIA_ROOT, 'gnn_graphs')
            os.makedirs(graph_dir, exist_ok=True)

            file_path = os.path.join(graph_dir, f'{transaction_id}.png')
            plt.savefig(file_path)
            plt.close()

            print(f"Successfully generated GNN graph at {file_path}")
            return os.path.join('media', 'gnn_graphs', f'{transaction_id}.png')

        except Transaction.DoesNotExist:
            print(f"Could not generate graph: Transaction {transaction_id} not found.")
            return None
        except Exception as e:
            print(f"An error occurred during graph generation: {e}")
            return None