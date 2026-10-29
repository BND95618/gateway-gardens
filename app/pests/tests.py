# /app/pests/tests.py

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.test                import TestCase
from django.urls                import reverse

from .models                    import Pest

# ------------------------------------------------------------------------------
# Web page access: Unauthenticated users
# > Redirecction to the 'index' page should occur
# ------------------------------------------------------------------------------
class UnauthenticatedUserPageAccessTest(TestCase):
    def test_pest_summary_page(self):
        print("Pests - Test 1.1: pest_summary test")

        url = reverse("pests:pest_summary")
        response = self.client.get("/pest_summary/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get(url).status_code, 302)
        self.assertEqual(response.url, '/')
    def test_pest_add_page(self):
        print("Pests - Test 1.2: pest_add test")

        url = reverse("pests:pest_add")
        response = self.client.get("/pest_add/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get(url).status_code, 302)
        self.assertEqual(response.url, '/')
# ------------------------------------------------------------------------------
# Web page access: Autenticated users with 'Gardener' group privileges
# > All pages in the pests app should be reachable
# ------------------------------------------------------------------------------
class AuthenticatedGardenerPageAccessTest(TestCase):
    #--------------------------------------------------------------------------------
    # pest setup
    #--------------------------------------------------------------------------------
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="Tester", password="tester-888!")
        cls.pest = Pest.objects.create(pest_name = "test pest",
                                       family    = "test family")
    def setUp(self):
        self.client.login(username="Tester", password="tester-888!")
        # Create a Group and add the user to it
        self.gardener_group = Group.objects.create(name="Gardener")
        self.user.groups.add(self.gardener_group)
    #--------------------------------------------------------------------------------
    # pest_summary view tests
    #--------------------------------------------------------------------------------
    def test_pest_summary_page(self):
        print("Pests - Test 2.1: pest_summary test")

        url = reverse("pests:pest_summary")
        response = self.client.get("/pest_summary/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTemplateUsed(response, "pests/pest_summary.html")
        self.assertContains(response, "<h1>Pests</h1>")
    #--------------------------------------------------------------------------------
    # pest_add view tests
    #--------------------------------------------------------------------------------
    def test_pest_add_page(self):
        print("Pests - Test 2.2: pest_add test")

        url = reverse("pests:pest_add")
        response = self.client.get("/pest_add/")
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get(url).status_code, 302)
        self.assertEqual(response.url, '/')
    #--------------------------------------------------------------------------------
    # pest_edit view tests
    #--------------------------------------------------------------------------------
    def test_pest_edit_page(self):
        print("Pests - Test 2.3: pest_edit test")

        url = reverse('pests:pest_delete', kwargs={'id': self.pest.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
    #--------------------------------------------------------------------------------
    # delete view tests
    #--------------------------------------------------------------------------------
    def test_pest_delete_page(self):
        print("Pests - Test 2.4: pest_delete test")

        url = reverse('pests:pest_delete', kwargs={'id': self.pest.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
# ------------------------------------------------------------------------------
# Web page access: Autenticated users with 'Garden-Editor' group privileges
# > All pages in the pests app should be reachable
# ------------------------------------------------------------------------------
class AuthenticatedGardenEditorPageAccessTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create the user and pest once
        cls.user = User.objects.create_user(username="Tester", password="tester-888!")
        cls.pest = Pest.objects.create(pest_name = "test pest",
                                       family    = "test family")
        # Setup groups and permissions here to keep tests isolated and fast
        cls.editors_group = Group.objects.create(name="Garden-Editor")
        cls.user.groups.add(cls.editors_group)
 
    def setUp(self):
        # force_login skips the expensive password-hashing backend step, speeding up tests
        self.client.force_login(self.user)
        # self.client.login(username="Tester", password="tester-888!")
    #--------------------------------------------------------------------------------
    # pest_summary view tests
    #--------------------------------------------------------------------------------
    def test_pest_summary_page(self):
        print("Pests - Test 3.1: pest_summary test")

        url = reverse("pests:pest_summary")
        response = self.client.get("/pest_summary/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTemplateUsed(response, "pests/pest_summary.html")
        self.assertContains(response, "<h1>Pests</h1>")
    #--------------------------------------------------------------------------------
    # pest_add view tests
    #--------------------------------------------------------------------------------
    def test_pest_add_page(self):
        print("Pests - Test 3.2: pest_add test")

        url = reverse("pests:pest_add")
        response = self.client.get("/pest_add/")
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get(url).status_code, 302)
    #--------------------------------------------------------------------------------
    # pest_edit view tests
    #--------------------------------------------------------------------------------
    def test_pest_edit_view_get_request(self):
        """Verify the pest_edit page loads and pre-populates the form with existing data."""
        print("Pests - Test 3.3: pest_edit test")

        # Make the page load request
        edit_url = reverse('pests:pest_edit', kwargs={'id': self.pest.id})

        # Create the view response
        response = self.client.get(edit_url)

        # Check that the page loads successfully
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pests/pest_edit.html')

        # Check that the form instance in the context contains the original data
        form = response.context['form']
        self.assertEqual(form.initial['pest_name'], "test pest")
        self.assertEqual(form.initial['family'],    "test family")
    
    def test_pest_edit_view_post_request(self):
        """Verify submits valid form data, updates the instance, and returns JSON response."""
        print("Pests - Test 3.4: pest_edit test")

        # Make the page load request
        edit_url = reverse('pests:pest_edit', kwargs={'id': self.pest.id})

        # Update the pest model information
        updated_data = {
            'pest_name' : "new test pest",
            'family'    : "new test family"
        }

        # Submit the new data via POST and receive response
        response = self.client.post(edit_url, data = updated_data)

        # Check Database State Change
        self.pest.refresh_from_db()

        self.assertEqual(self.pest.pest_name, "new test pest")
        self.assertEqual(self.pest.family,    "new test family")

        # Check response status code
        self.assertEqual(response.status_code, 200)
        
        # Extract and check the JSON response body
        response_data = response.json()
        self.assertEqual(response_data["status"], "success")
        self.assertEqual(response_data["message"], "Edited pest successfully")

        # The subsequent Javascript will redirect to pest_details.  
        # This is outside of the Django testing.
    #--------------------------------------------------------------------------------
    # pest_delete view tests
    #--------------------------------------------------------------------------------
    def test_pest_delete_view_renders_modal_get(self):
        """A GET request should return a 200 status and not delete the item."""
        # Create a pest db record
        self.pest = Pest.objects.create(pest_name = "test delete pest",
                                        family    = "test delete family")
        # Make the page load request to the Django view and capture the response
        delete_url = reverse('pests:pest_delete', kwargs={'id': self.pest.id})
        response = self.client.get(delete_url)
        # Ensure the pest stillexists in the database
        self.assertTrue(Pest.objects.filter(id = self.pest.id).exists())
        # Ensure correct response code
        self.assertEqual(response.status_code, 200)
        # Ensure the right template is rendered
        self.assertTemplateUsed(response, "pests/pest_delete_modal.html")
        # Ensure the pest object is present in the template context
        self.assertEqual(response.context["pest"], self.pest)
    
    def test_pest_delete(self):
        """  """
        print("Pests - Test 3.5: pest_delete test")
        # Create a pest db record
        self.pest = Pest.objects.create(pest_name = "test delete pest",
                                        family    = "test delete family")
        # Check that the pest is in the db
        self.assertTrue(Pest.objects.filter(id = self.pest.id).exists())
        # Make the page load request to the Django view and capture the response
        delete_url = reverse('pests:pest_delete', kwargs={'id': self.pest.id})
        response = self.client.post(delete_url)
        # Verify the record is completely removed from the database
        self.assertFalse(Pest.objects.filter(id = self.pest.id).exists())
        # Check response status code (302 = redirect)
        self.assertRedirects(response, reverse('pests:pest_summary'))
    
    def test_pest_delete_nonexistent_pest_returns_404(self):
        """ Attempting to delete a non-existent item primary key must return a 404."""
        print("Pests - Test 3.6: pest_delete non-existent item test")
        invalid_url = reverse('pests:pest_delete', kwargs={'id': 99999})
        response = self.client.post(invalid_url)
        self.assertEqual(response.status_code, 404)
    #--------------------------------------------------------------------------------
    # pest model tests
    #--------------------------------------------------------------------------------
    def test_pest_model(self):
        print("Pests - Test 3.5: pest model add/access db contents")
        self.assertEqual(self.pest.pest_name,          "test pest")
        self.assertEqual(self.pest.family,             "test family")
        self.assertEqual(self.pest.get_absolute_url(), "/pest_summary/")
    #--------------------------------------------------------------------------------