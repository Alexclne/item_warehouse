from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from .views import PersonalListCreateAPIView, personal_list_view, detail_view, registration,login_view, new_logout, lista_profumi

urlpatterns = [

    path("articles/",PersonalListCreateAPIView.as_view(), name="personal-list"),
    path("articles/html/", personal_list_view, name="personal_list_html"),
    path("articles/html/profumi", lista_profumi, name= "profumes_list"),
    path("articles/html/detail/<int:pk>/", detail_view, name="detail_list_html"),
    
        #AUTH PATH
    path("accounts/", include("django.contrib.auth.urls")),#importato da django doc
    path('registration/', registration , name='registration' ), 
    path('login/',login_view, name='login'),
    path('logout/', new_logout, name='logout'),

]
if settings.DEBUG:  # Solo durante lo sviluppo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)