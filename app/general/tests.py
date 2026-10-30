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
        print("General - Test 1.1: Index test")

        url = reverse("general:index")
        response = self.client.get("/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTemplateUsed(response, "general/index.html")
        self.assertContains(response, "<h1>Garden/Plant Web Site</h1>")
    def test_glossary_page(self):
        print("General - Test 1.2: Glossary test")

        url = reverse("general:glossary")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_reference_page(self):
        print("General - Test 1.3: Reference test")

        url = reverse("general:reference")
        response = self.client.get("/reference/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get(url).status_code, 302)
        self.assertEqual(response.url, '/')
    def test_about_page(self):
        print("General - Test 1.4: About test")
              
        url = reverse("general:about")
        response = self.client.get("/about/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get(url).status_code, 302)
        self.assertEqual(response.url, '/')
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
        print("General - Test 2.1: Index test")

        url = reverse("general:index")
        response = self.client.get("/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTemplateUsed(response, "general/index.html")
        self.assertContains(response, "<h1>Garden/Plant Web Site</h1>")
    def test_glossary_page(self):
        print("General - Test 2.2 Glossary test")

        url = reverse("general:glossary")
        response = self.client.get("/glossary/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTemplateUsed(response, "general/glossary.html")
        self.assertContains(response, "<h1>Glossary</h1>")
    def test_reference_page(self):
        print("General - Test 2.3: Reference test")

        url = reverse("general:reference")
        response = self.client.get("/reference/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTemplateUsed(response, "general/reference.html")
        self.assertContains(response, "<h1>Reference</h1>")
    def test_about_page(self):
        print("General - Test 2.4: About test")

        url = reverse("general:about")
        response = self.client.get("/about/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(url).status_code, 200)
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
        print("General - Test 3.1: Index test")

        url = reverse("general:index")
        response = self.client.get("/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTemplateUsed(response, "general/index.html")
        self.assertContains(response, "<h1>Garden/Plant Web Site</h1>")
    def test_glossary_page(self):
        print("General - Test 3.2: Glossary test")

        url = reverse("general:glossary")
        response = self.client.get("/glossary/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTemplateUsed(response, "general/glossary.html")
        self.assertContains(response, "<h1>Glossary</h1>")
    def test_reference_page(self):
        print("General - Test 3.3: Reference test")

        url = reverse("general:reference")
        response = self.client.get("/reference/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTemplateUsed(response, "general/reference.html")
        self.assertContains(response, "<h1>Reference</h1>")
    def test_about_page(self):
        print("General - Test 3.4: About test")

        url = reverse("general:about")
        response = self.client.get("/about/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTemplateUsed(response, "general/about.html")
        self.assertContains(response, "<h1>About</h1>")
# ------------------------------------------------------------------------------
