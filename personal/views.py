from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from django.views.generic import ListView

from .models import Article
from .serializer import PersonalSerializer
# Create your views here.

class PersonalListCreateAPIView(APIView):

    def get(self, request):
        name_filter = request.query_params.get('name', None)  # Ottieni il valore del parametro 'name' dalla query string
        if name_filter:
            personal = Article.objects.filter(name__icontains=name_filter)  # Filtro per nome (case-insensitive)
        else:
            personal = Article.objects.all()

        serializer = PersonalSerializer(personal, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PersonalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#________________________________________________________________________________#
class PersonalDetailAPIView(APIView):

    def get_object(self, pk):
        article= get_object_or_404(Article, pk=pk)
        return article
    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = PersonalSerializer(article)
        return Response(serializer.data)
    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = PersonalSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)       

def personal_list_view(request):
    articles = Article.objects.all()  # Ottieni tutti gli articoli
    return render(request, 'personal/home.html', {'articles': articles})