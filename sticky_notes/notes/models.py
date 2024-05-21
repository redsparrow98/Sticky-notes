from django.db import models

class Note(models.Model):
    """
    Model representing a note.
    
    Fields:
    - title: CharFiled to post the tile of the note.
    - content = TextField to post the content of the note.
    - created_at = DateTimeField set to the current date of creating the note.
    
    Relationship:
    - author: ForeignKey representing the author of the post
    
    Methods:
    - a return string for the title of the note
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        String for representing the Note object (title).
        """
        return self.title


class Author(models.Model):
    """
    Model representing an author.
    
    Field:
    -name: CharField for the authors name
    
    Method:
    - a method to return the name of the Author
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        """
        String for representing the Author object (name).
        """
        return self.name
