from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse , Http404
import os


def get_gnn_graph_image(request , transaction_id):

    try:
        image_path = os.path.join(
            settings.MEDIA_ROOT, 'gnn_graphs' , f'{transaction_id}.png'
        )
        if os.path.exists(image_path):
            return FileResponse(open(image_path , 'rb'), content_type='image/png')
        else:
            raise Http404("GNN graph not found for this transaction.")

    except Exception as e:
        raise Http404(str(e))

