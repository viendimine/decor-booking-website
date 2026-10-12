from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="index"),
    path("past-work/", views.gallery, name="gallery"),
    path("book/", views.book, name="book"),
    path("booked/<str:reference>/", views.booked, name="booked"),
]
