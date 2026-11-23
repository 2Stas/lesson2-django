from django.urls import path
from . import views

urlpatterns = [
    path("", views.map_page, name="map_page"),
    path("create-location/", views.create_location, name="create_location"),
               
]
