from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="list"),
	path('notes/<str:pk>/', views.notes, name="notes"),
	path('dashboard/', views.dashboard, name="dashboard"),
	path('public/', views.public, name="public"),
	path('private/', views.private, name="private"),
    path("handlerequest/", views.handlerequest, name="handleRequest"),
	path('edit/', views.edit, name="edit"),
	path('basic/', views.basic, name="basic"),
	path('update_task/<str:pk>/', views.updateTask, name="update_task"),
	path('delete/<str:pk>/', views.deleteTask, name="delete"),
]