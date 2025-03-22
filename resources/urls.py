# import path from django
from django.urls import path
from .views import ResourceListView, ResourceDetailView, ResourceDownloadView

urlpatterns = [
    path('', ResourceListView.as_view(), name='resource-list'),
    path('<int:pk>/', ResourceDetailView.as_view(), name='resource-detail'),
    path('<int:pk>/download/', ResourceDownloadView.as_view(), name='resource-download'),
]