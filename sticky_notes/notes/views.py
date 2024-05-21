from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, Author
from django.utils import timezone


def index(request):
    """
    Display a list of all notes.
    
    This function retrieves all notes from the database 
    and renders the 'index.html' template with the list of notes.
    """
    # Retrieve all notes from the database
    notes = Note.objects.all()
    # Render the 'index.html' template with the list of notes
    return render(request, 'notes/index.html', {'notes': notes})


def add_note(request):
    """
    Add a new note.

    This function handles both GET and POST requests. 
    For a GET request, it renders the 'add_note.html' template.
    For a POST request, it processes the form data, creates a new note, 
    and redirects to the home page.
    """
    # If the request method is POST, process the form data
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author_name = request.POST.get('author_name')
        
        # Get or create the author based on the provided name
        author, created = Author.objects.get_or_create(name=author_name)
        
        # Create a new note with the provided data
        Note.objects.create(title=title, content=content, author=author, created_at=timezone.now())
        
        # Redirect to the home page after adding the note
        return redirect('index')
    
    # If the request method is GET, render the 'add_note.html' template
    return render(request, 'notes/add_note.html')


def view_note(request, note_id):
    """
    View details of a specific note.

    This function retrieves the note with the given ID from the database 
    and renders the 'view_note.html' template with the note details.
    """
    # Retrieve the note object from the database based on the provided ID
    note = get_object_or_404(Note, id=note_id)
    # Render the 'view_note.html' template with the note details
    return render(request, 'notes/view_note.html', {'note': note})


def edit_note(request, note_id):
    """
    Edit an existing note.

    This function retrieves the note with the given ID from the database 
    and handles form submission to edit the note details.
    """
    # Retrieve the note object from the database based on the provided ID
    note = get_object_or_404(Note, id=note_id)
    
    # If the request method is POST, process the form data
    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.save()
        # Redirect to the home page after editing the note
        return redirect('index')
    
    # If the request method is GET, render the 'edit_note.html' template
    return render(request, 'notes/edit_note.html', {'note': note})


def delete_note(request, note_id):
    """
    Delete an existing note.

    This function retrieves the note with the given ID from the database 
    and deletes it, then redirects to the home page.
    """
    # Retrieve the note object from the database based on the provided ID
    note = get_object_or_404(Note, id=note_id)
    # Delete the note from the database
    note.delete()
    # Redirect to the home page after deleting the note
    return redirect('index')

def author_notes(request, author_id):
    """
    View to display all notes by a specific author.
    """
    author = get_object_or_404(Author, id=author_id)
    notes = Note.objects.filter(author=author)
    return render(request, 'notes/author_notes.html', {'author': author, 'notes': notes})

def search_author(request):
    """
    View to handle searching for notes by an author's name.
    """
    author_name = request.GET.get('author_name')
    if author_name:
        authors = Author.objects.filter(name__icontains=author_name)
        return render(request, 'notes/search_results.html', {'authors': authors})
    else:
        return redirect('index')
