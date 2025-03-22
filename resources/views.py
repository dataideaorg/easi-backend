from django.shortcuts import render
from rest_framework import viewsets
from .models import Resource
from .serializers import ResourceSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse

# views to get all resources and download a resource
class ResourceListView(APIView):
    def get(self, request):
        resources = Resource.objects.all()
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)
    
class ResourceDetailView(APIView):
    def get(self, request, pk):
        resource = Resource.objects.get(pk=pk)
        serializer = ResourceSerializer(resource)
        return Response(serializer.data)
    
class ResourceDownloadView(APIView):
    def get(self, request, pk):
        resource = Resource.objects.get(pk=pk)
        response = FileResponse(resource.file)
        response['Content-Disposition'] = f'attachment; filename="{resource.file.name}"'
        return response


