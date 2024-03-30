from django.urls import path
from . import views



#urlconfig
urlpatterns = [
    path('myphoto/', views.say_hello)
]