from django.urls import path
from .views import get_gnn_graph_image

urlpatterns = [
    path('graph/<uuid:transaction_id>/', get_gnn_graph_image, name='gnn-graph-image'),
]