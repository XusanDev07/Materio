from django.urls import path
from materio.views import Main

urlpatterns = [
    path('main/', Main.as_view()),
]