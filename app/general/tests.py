# /app/general/tests.py

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.test                import TestCase
from django.urls                import reverse

# ------------------------------------------------------------------------------
# Web page access: Unauthenticated users
# > Only the 'index' page should be reachable
# ------------------------------------------------------------------------------
class UnauthenticatedUserPageAccessTest(TestCase):
    def test_home_page(self):
        """Test that the index view renders successfully with the correct template and content."""
        url = reverse("general:index")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "general/index.html")
        self.assertContains(response, "<h1>Garden/Plant Web Site</h1>")
        
    def test_glossary_page_redirects(self):
        """Test that the glossary page issues a 302 redirect to the home page."""
        url = reverse("general:glossary")
        response = self.client.get(url)
        
        # Streamlined: Asserts 302 status code and target URL in one clean step
        self.assertRedirects(response, reverse("general:index"))

    def test_reference_page_redirects(self):
        """Test that the reference page issues a 302 redirect to the home page."""
        url = reverse("general:reference")
        response = self.client.get(url)
        
        # Streamlined: Asserts 302 status code and target URL in one clean step
        self.assertRedirects(response, reverse("general:index"))

    def test_about_page_redirects(self):
        """Test that the about page issues a 302 redirect to the home page."""
        url = reverse("general:about")
        response = self.client.get(url)
        
        # Streamlined: Asserts 302 status code and target URL in one clean step
        self.assertRedirects(response, reverse("general:index"))

# ------------------------------------------------------------------------------
# Web page access: Autenticated users with 'Gardener' group privileges
# > All pages in the general app should be reachable
# ------------------------------------------------------------------------------
class AuthenticatedGardenerPageAccessTest(TestCase):
    @classmethod
    
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="Tester", password="tester-888!")
    
    def setUp(self):
        self.client.login(username="Tester", password="tester-888!")
        # Create a Group and add the user to it
        self.gardener_group = Group.objects.create(name="Gardener")
        self.user.groups.add(self.gardener_group)
    
    def test_home_page(self):
        """Test that the index view renders successfully with the correct template and content."""
        url = reverse("general:index")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "general/index.html")
        self.assertContains(response, "<h1>Garden/Plant Web Site</h1>")
    
    def test_glossary_page(self):
        """Test that the glossary view renders successfully with the correct template and content."""
        url = reverse("general:glossary")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "general/glossary.html")
        self.assertContains(response, "<h1>Glossary</h1>")
    
    def test_reference_page(self):
        """Test that the reference view renders successfully with the correct template and content."""
        url = reverse("general:reference")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "general/reference.html")
        self.assertContains(response, "<h1>Reference</h1>")
      
    def test_about_page(self):
        """Test that the about view renders successfully with the correct template and content."""
        url = reverse("general:about")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "general/about.html")
        self.assertContains(response, "<h1>About</h1>")
    
# ------------------------------------------------------------------------------
# Web page access: Autenticated users with 'Garden-Editor' group privileges
# > All pages in the general app should be reachable
# ------------------------------------------------------------------------------
class AuthenticatedGardenEditorPageAccessTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="Tester", password="tester-888!")
    
    def setUp(self):
        # Log in the user
        self.client.login(username="Tester", password="tester-888!")
        # Create a Group and add the user to it
        self.editors_group = Group.objects.create(name="Garden-Editor")
        self.user.groups.add(self.editors_group)
  
    def test_home_page(self):
        """Test that the index view renders successfully with the correct template and content."""
        url = reverse("general:index")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "general/index.html")
        self.assertContains(response, "<h1>Garden/Plant Web Site</h1>")
    
    def test_glossary_page(self):
        """Test that the glossary view renders successfully with the correct template and content."""
        url = reverse("general:glossary")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "general/glossary.html")
        self.assertContains(response, "<h1>Glossary</h1>")
    
    def test_reference_page(self):
        """Test that the reference view renders successfully with the correct template and content."""
        url = reverse("general:reference")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "general/reference.html")
        self.assertContains(response, "<h1>Reference</h1>")
      
    def test_about_page(self):
        """Test that the about view renders successfully with the correct template and content."""
        url = reverse("general:about")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "general/about.html")
        self.assertContains(response, "<h1>About</h1>")
    
# ------------------------------------------------------------------------------