from django.urls import path
from . import views


# URL patterns for the notes app
urlpatterns = [
    # Path for the home page
    path('', views.index, name='index'),

    # Path for adding a new note
    path('add/', views.add_note, name='add_note'),

    # Path for viewing details of a specific note
    path('note/<int:note_id>/', views.view_note, name='view_note'),

    # Path for editing an existing note
    path('note/<int:note_id>/edit/', views.edit_note, name='edit_note'),

    # Path for deleting an existing note
    path('note/<int:note_id>/delete/', views.delete_note, name='delete_note'),

	# Path to view all notes of a specific author
	path('author/<int:author_id>/', views.author_notes, name='author_notes'),#

	path('search/', views.search_author, name='search_author'),
]
