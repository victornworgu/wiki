from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("wiki/<str:title>", views.view_entry, name="viewentry"),
	path("search", views.search, name="search"),
	path("addnew", views.addnew, name="addnew"),
	path("random", views.random, name="random"),
	path("edit/<str:title>", views.edit, name="edit")
]
