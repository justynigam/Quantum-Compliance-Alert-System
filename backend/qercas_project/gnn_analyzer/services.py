import os
import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend before importing pyplot
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
            center_tx = Transaction.objects.get(id=transaction_id)
            
            # --- THIS IS THE CORRECTED LOGIC ---
            # 1. Get the accounts involved in our main transaction.
            accounts_in_tx = [center_tx.source_account, center_tx.destination_account]
            
            # 2. Find all other transactions that involve EITHER of these accounts.
            related_txns = Transaction.objects.filter(
                Q(source_account__in=accounts_in_tx) |
                Q(destination_account__in=accounts_in_tx)
            ).exclude(id=transaction_id).distinct()[:10] # Limit to 10 for readability

            # 3. Build the graph
            G = nx.Graph()
            
            # Add all unique accounts from all related transactions as nodes
            all_accounts = {center_tx.source_account, center_tx.destination_account}
            for tx in related_txns:
                all_accounts.add(tx.source_account)
                all_accounts.add(tx.destination_account)
            
            for acc in all_accounts:
                G.add_node(acc)

            # Add edges for the main transaction and all related ones
            G.add_edge(center_tx.source_account, center_tx.destination_account)
            for tx in related_txns:
                G.add_edge(tx.source_account, tx.destination_account)

            # 4. Generate and save the graph image
            # Use thread-safe figure creation
            fig, ax = plt.subplots(figsize=(10, 7))
            pos = nx.spring_layout(G, k=0.8) # Adjust layout spacing
            nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, 
                    edge_color='gray', font_size=10, font_weight='bold', ax=ax)
            
            graph_dir = os.path.join(settings.MEDIA_ROOT, 'gnn_graphs')
            os.makedirs(graph_dir, exist_ok=True)

            graph_filename = f"{transaction_id}.png"
            graph_path = os.path.join(graph_dir, graph_filename)
            
            # Save and close properly to avoid memory leaks
            fig.savefig(graph_path, dpi=150, bbox_inches='tight')
            plt.close(fig)  # Explicitly close the figure
            
            print(f"Successfully generated GNN graph at {graph_path}")
            return os.path.join('media', 'gnn_graphs', graph_filename)

        except Transaction.DoesNotExist:
            print(f"Transaction {transaction_id} not found.")
            return None
        except Exception as e:
            print(f"An error occurred during graph generation: {e}")
            return None
