from django.urls import path, include

from django.urls import path
from .views import PersonalListCreateAPIView, personal_list_view

urlpatterns = [

    path("articles/",PersonalListCreateAPIView.as_view(), name="personal-list"),
    path("articles/html/", personal_list_view, name="personal_list_html"),
]