from django.contrib import admin
from .models import Note
from .models import Author

# Register your models here.

# Notes mode
admin.site.register(Note)

# Author model
admin.site.register(Author)
