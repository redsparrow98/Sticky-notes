from django.test import TestCase, Client
from django.urls import reverse
from .models import Note, Author
from django.utils import timezone

# Create your tests here.


# Model Tests
class NoteModelTests(TestCase):
    def setUp(self):
        # Create an Author object to associate with the Note for testing
        self.author = Author.objects.create(name="Test Author")
        
        # Create a Note object for testing
        self.note = Note.objects.create(
            title="Test Note",
            content="This is a test note.",
            created_at=timezone.now(),
            author=self.author
        )


    def test_note_creation(self):
        """
        Test that a Note object is correctly created with all the attributes.
        """
        self.assertEqual(self.note.title, "Test Note")
        self.assertEqual(self.note.content, "This is a test note.")
        self.assertEqual(self.note.author.name, "Test Author")

class AuthorModelTests(TestCase):
    def setUp(self):
        # Create an Author object for testing
        self.author = Author.objects.create(name="Test Author")


    def test_author_creation(self):
        """
        Test that an Author object is correctly created with the name attribute.
        """
        self.assertEqual(self.author.name, "Test Author")


# -------------------------------------------------------------------------------------------------------------
# View Tests
class NoteViewTests(TestCase):
    def setUp(self):
        # Set up the test client
        self.client = Client()

        # Create an Author instance
        self.author = Author.objects.create(name="Test Author")

        # Create a Note instance
        self.note = Note.objects.create(
            title="Test Note",
            content="This is a test note.",
            created_at=timezone.now(),
            author=self.author
        )


    def test_index_view(self):
        """
        Test the index view to ensure it loads correctly.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")


    def test_add_note_view(self):
        """
        Test adding a new note through the add_note view.
        """
        response = self.client.post(reverse('add_note'), {
            'title': 'Another Test Note',
            'content': 'This is another test note.',
            'author_name': 'Another Test Author'
        })

        # Check for redirect
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Note.objects.filter(title='Another Test Note').exists())


    def test_view_note_view(self):
        """
        Test viewing a single note.
        """
        response = self.client.get(reverse('view_note', args=[self.note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.note.title)


    def test_edit_note_view(self):
        """
        Test editing an existing note.
        """
        response = self.client.post(reverse('edit_note', args=[self.note.id]), {
            'title': 'Updated Test Note',
            'content': 'This note has been updated.'
        })
        
        # Check for redirect
        self.assertEqual(response.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Test Note')


    def test_delete_note_view(self):
        """
        Test deleting a note.
        """
        response = self.client.post(reverse('delete_note', args=[self.note.id]))
        
        # Check for redirect
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())


    def test_list_author_notes_view(self):
        """
        Test listing notes by a specific author.
        """
        response = self.client.get(reverse('author_notes', args=[self.author.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.note.title)
        self.assertContains(response, self.author.name)


    def test_search_authors_view(self):
        """
        Test searching for authors.
        """
        response = self.client.get(reverse('search_authors') + '?q=Test Author')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.author.name)

        # Test no results
        response = self.client.get(reverse('search_authors') + '?q=Nonexistent Author')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.author.name)
