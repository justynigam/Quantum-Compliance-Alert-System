from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse, Http404
import os
from .services import GNNService


def get_gnn_graph_image(request, transaction_id):
    try:
        image_path = os.path.join(
            settings.MEDIA_ROOT, 'gnn_graphs', f'{transaction_id}.png'
        )
        
        # If the graph doesn't exist, generate it
        if not os.path.exists(image_path):
            print(f"GNN graph not found for transaction {transaction_id}, generating...")
            result = GNNService.analyze_and_generate_graph(transaction_id)
            if not result:
                raise Http404("Could not generate GNN graph for this transaction.")
        
        # Now check again if the file exists
        if os.path.exists(image_path):
            return FileResponse(open(image_path, 'rb'), content_type='image/png')
        else:
            raise Http404("GNN graph not found for this transaction.")

    except Exception as e:
        print(f"Error in get_gnn_graph_image: {e}")
        raise Http404(str(e))
