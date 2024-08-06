from django.urls import path
from ideaVaultApi import views

urlpatterns = [
    path("", views.ideas),
    path("<int:id>", views.ideas_id),
]
