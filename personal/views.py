from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


from .models import Article, Categoria
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

def personal_list_view(request, category_name=None):
    if category_name:
        # Filtra gli articoli in base alla categoria selezionata
        articles = Article.objects.filter(categoria__nome=category_name)
    else:
        # Se non è specificata una categoria, mostra tutti gli articoli
        articles = Article.objects.all()

    # Aggiungi tutte le categorie per poterle visualizzare nel template
    categories = Categoria.objects.all()

    # Passa gli articoli filtrati e le categorie al template
    return render(request, 'personal/home.html', {'articles': articles, 'categories': categories})

def detail_view(request,pk):
    articles = get_object_or_404(Article, pk=pk)
    return render(request, 'personal/detail.html', {'article': articles})

#INIZIO DELLA SEZIONE RELATIVA ALLA VISTA 'PROFUMI'

def lista_profumi(request):
    # Filtra gli articoli la cui categoria ha il nome "Profumi"
    profumi  = Article.objects.filter(categoria__nome="Profumi")
    
    return render(request, "personal/profumi.html", {"profumi": profumi})

#SEZIONE RELATICA ALL'AUTENTICAZIONE DELL'UTENTE
def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('personal_list_html')
    else:
        form = UserCreationForm()

    # Mostra solo gli errori dopo il submit
    return render(request, "registration/registration.html", {"form": form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('personal_list_html'))
        else:
            return render(request, 'registration/login.html', {'error': 'Credenziali non valide'})
    return render(request, 'registration/login.html')

def new_logout(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseRedirect(reverse('personal_list_html'))
#FINE DELLA SEZIONE RELATIVA ALL'AUTENTICAZIONE DELL'UTENTE


