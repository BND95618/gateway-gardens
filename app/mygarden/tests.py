from django.test import TestCase

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.test                import TestCase
from django.urls                import reverse

from .models                    import Garden

# ------------------------------------------------------------------------------
# Web page access: Unauthenticated users
# > Only the 'index' page should be reachable
# ------------------------------------------------------------------------------
class UnauthenticatedUserPageAccessTest(TestCase):
    def test_mygarden_summary_page_redirects(self):
        """Test that the My Garden Summary page issues a 302 redirect to the home page."""
        # Get the url and create the response
        url = reverse("mygarden:mygarden_summary")
        response = self.client.get(url)
        
        # Streamlined: Asserts 302 status code and target URL in one clean step
        self.assertRedirects(response, reverse("general:index"))

    def test_mygarden_add_page_redirects(self):
        """Test that the My Garden Add page issues a 302 redirect to the home page."""
        # Get the url and create the response
        url = reverse("mygarden:mygarden_add")
        response = self.client.get(url)
        
        # Streamlined: Asserts 302 status code and target URL in one clean step
        self.assertRedirects(response, reverse("general:index"))

    def test_mygarden_edit_page_redirects(self):
        """Test that the My Garden Edit page issues a 302 redirect to the home page."""
        # Get the url and create the response
        url = reverse('mygarden:mygarden_edit', kwargs={'id': 1})
        response = self.client.get(url)
        
        # Streamlined: Asserts 302 status code and target URL in one clean step
        self.assertRedirects(response, reverse("general:index"))

# ------------------------------------------------------------------------------
# Web page access: Autenticated users with 'Gardener' group privileges
# ------------------------------------------------------------------------------
class AuthenticatedGardenerPageAccessTest(TestCase):
    @classmethod
    
    def setUpTestData(cls):
        # Setup the test user
        cls.username = "test-user"
        cls.password = "tester-888!"
        # Create user
        cls.user = User.objects.create_user(username=cls.username, password=cls.password)
        # Create the user's garden
        cls.garden = Garden.objects.create(
            owner = cls.username,
            name  = "test-name",
            city  = "test-city",
            state = "test-state"
        )
        
    def setUp(self):
        # Log in using the exact credentials created in setUpTestData
        logged_in = self.client.login(username=self.username, password=self.password)
        # Check that the login was successful
        self.assertTrue(logged_in, "Client login failed.")  
        
        # Handle your Group setup
        self.gardener_group = Group.objects.create(name="Gardener")
        self.user.groups.add(self.gardener_group)
        
    def test_mygarden_summary_page(self):
        """Test that the My Garden Summary view renders successfully with the correct template and content."""
        # Get the url and create the response
        url = reverse("mygarden:mygarden_summary")
        response = self.client.get(url)
        
        # Check that the page loaded successfully with status code = 200
        self.assertEqual(response.status_code, 200)
        # Check that the correct template was used
        self.assertTemplateUsed(response, "mygarden/mygarden_summary.html")
        # Check context data
        self.assertEqual(response.context['garden'], self.garden)
        self.assertEqual(len(response.context['image_fields']), 8)

    def test_mygarden_add_post_redirect(self):
        """Test that the My Garden Add view executes since request is via POST"""
        # Get the url and create the response
        url = reverse("mygarden:mygarden_add")
        response = self.client.post(url)
        
        # Check that the redirected successfully with status code = 302
        self.assertEqual(response.status_code, 302)

    def test_mygarden_add_get_error_redirect(self):
        """Test that the My Garden Add view does not execute since request is not via POST"""
        # Get the url and create the response
        url = reverse("mygarden:mygarden_add")
        response = self.client.get(url)
        
        # Check that the redirected successfully with status code = 405
        self.assertEqual(response.status_code, 405)
        
    def test_mygarden_edit_view_get_request(self):
        """Verify the pest_edit page loads and pre-populates the form with existing data."""
        # Get the url and create the response
        url = reverse('mygarden:mygarden_edit', kwargs={'id': self.garden.id})
        response = self.client.get(url)

        # Check that the page loads successfully
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mygarden/mygarden_edit.html')

        # Check that the form instance in the context contains the original data
        form = response.context['form']
        self.assertEqual(form.initial['name'],  "test-name")
        self.assertEqual(form.initial['city'],  "test-city")
        self.assertEqual(form.initial['state'], "test-state")

    def test_mygarden_edit_view_post_request(self):
        """Verify submits valid form data, updates the instance, and returns JSON response."""
        # Make the page load request
        url = reverse('mygarden:mygarden_edit', kwargs={'id': self.garden.id})

        # Update the garden model information
        updated_data = {
            'name'  : "new-test-name",
            'city'  : "new-test-city",
            'state' : "new-test-state"
        }

        # Submit the new data via POST and receive response
        response = self.client.post(url, data = updated_data)

        # Check Database State Change
        self.garden.refresh_from_db()

        self.assertEqual(self.garden.name,  "new-test-name")
        self.assertEqual(self.garden.city,  "new-test-city")
        self.assertEqual(self.garden.state, "new-test-state")

        # Check response status code
        self.assertEqual(response.status_code, 200)
        
        # Extract and check the JSON response body
        response_data = response.json()
        self.assertEqual(response_data["status"], "success")
        self.assertEqual(response_data["message"], "Edited My Garden successfully")

        # The subsequent Javascript will redirect to garden_details.  
        # This is outside of the Django testing.

# ------------------------------------------------------------------------------
# Web page access: Autenticated users with 'Garden-Editor' group privileges
# ------------------------------------------------------------------------------
class AuthenticatedGardenEditorPageAccessTest(TestCase):
    @classmethod
    
    def setUpTestData(cls):
        # Setup the test user
        cls.username = "test-user"
        cls.password = "tester-888!"
        # Create user
        cls.user = User.objects.create_user(username=cls.username, password=cls.password)
        # Create the user's garden
        cls.garden = Garden.objects.create(
            owner=cls.username,
            name="test-name",
            city="test-city",
            state="test-state"
        )
        
    def setUp(self):
        # Log in using the exact credentials created in setUpTestData
        logged_in = self.client.login(username=self.username, password=self.password)
        # Check that the login was successful
        self.assertTrue(logged_in, "Client login failed.")  
        
        # Handle your Group setup
        self.gardener_group = Group.objects.create(name="Garden-Editor")
        self.user.groups.add(self.gardener_group)
        
    def test_mygarden_summary_page(self):
        """Test that the My Garden Summary view renders successfully with the correct template and content."""
        # Get the url and create the response
        url = reverse("mygarden:mygarden_summary")
        response = self.client.get(url)
        
        # Check that the page loaded successfully with status code = 200
        self.assertEqual(response.status_code, 200)
        # Check that the correct template was used
        self.assertTemplateUsed(response, "mygarden/mygarden_summary.html")
        # Check context data
        self.assertEqual(response.context['garden'], self.garden)
        self.assertEqual(len(response.context['image_fields']), 8)

    def test_mygarden_add_post_redirect(self):
        """Test that the My Garden Add view executes since request is via POST"""
        # Get the url and create the response
        url = reverse("mygarden:mygarden_add")
        response = self.client.post(url)
        
        # Check that the redirected successfully with status code = 302
        self.assertEqual(response.status_code, 302)

    def test_mygarden_add_get_error_redirect(self):

        """Test that the My Garden Add view does not execute since request is not via POST"""
        # Get the url and create the response
        url = reverse("mygarden:mygarden_add")
        response = self.client.get(url)
        
        # Check that the redirected successfully with status code = 405
        self.assertEqual(response.status_code, 405)

    def test_mygarden_edit_view_get_request(self):
        """Verify the pest_edit page loads and pre-populates the form with existing data."""
        # Get the url and create the response
        url = reverse('mygarden:mygarden_edit', kwargs={'id': self.garden.id})
        response = self.client.get(url)

        # Check that the page loads successfully
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mygarden/mygarden_edit.html')

        # Check that the form instance in the context contains the original data
        form = response.context['form']
        self.assertEqual(form.initial['name'],  "test-name")
        self.assertEqual(form.initial['city'],  "test-city")
        self.assertEqual(form.initial['state'], "test-state")

    def test_mygarden_edit_view_post_request(self):
        """Verify submits valid form data, updates the instance, and returns JSON response."""
        # Make the page load request
        url = reverse('mygarden:mygarden_edit', kwargs={'id': self.garden.id})

        # Update the garden model information
        updated_data = {
            'name'  : "new-test-name",
            'city'  : "new-test-city",
            'state' : "new-test-state"
        }

        # Submit the new data via POST and receive response
        response = self.client.post(url, data = updated_data)

        # Check Database State Change
        self.garden.refresh_from_db()

        self.assertEqual(self.garden.name,  "new-test-name")
        self.assertEqual(self.garden.city,  "new-test-city")
        self.assertEqual(self.garden.state, "new-test-state")

        # Check response status code
        self.assertEqual(response.status_code, 200)
        
        # Extract and check the JSON response body
        response_data = response.json()
        self.assertEqual(response_data["status"], "success")
        self.assertEqual(response_data["message"], "Edited My Garden successfully")

        # The subsequent Javascript will redirect to garden_details.  
        # This is outside of the Django testing.
# ------------------------------------------------------------------------------