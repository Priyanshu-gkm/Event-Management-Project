from django.test import TestCase , Client
from django.urls import reverse
from accounts.models import Account

class TestAccountViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = Account.objects.create(email="attendeeTest@gmail.com",
                    username = "attendeeTest",
                    password= "Test@Abcd",
                    fname= "att3",
                    lname= "dee3",
                    gender= "Female",
                    role= "ORGANIZER")
        
        
    def test_AccountCreateView_POST_fail(self):
        # create account fail - username already exists
        data = {
                    "email": "attendeeTest@gmail.com",
                    "username": "attendeeTest",
                    "password": "Test@Abcd",
                    "fname": "att3",
                    "lname": "dee3",
                    "gender": "Female",
                    "role": "ORGANIZER",
                }
        response = self.client.post(reverse('LC_account'),data)
        self.assertEquals(response.status_code, 400)
        
    def test_AccountCreateView_POST_pass(self):
        # create account successful
        data = {
                    "email": "OrganizerTest@gmail.com",
                    "username": "OrganizerTest",
                    "password": "Test@Abcd",
                    "fname": "att3",
                    "lname": "dee3",
                    "gender": "Female",
                    "role": "ORGANIZER",
                }
        response = self.client.post(reverse('LC_account'),data)
        self.assertEquals(response.status_code, 201)
       
        
    def test_AccountListView_GET_pass(self):
        # list all account success 
        response = self.client.get(reverse('LC_account'))
        self.assertEquals(response.status_code, 200)
        
    def test_AccountRetrieveView_Get_fail(self):
        # id not found
        response = self.client.get(reverse('RUD_account',args=[70]))
        self.assertEqual(response.status_code,404)
    
    def test_AccountRetrieveView_Get_pass(self):
        # id found
        response = self.client.get(reverse('RUD_account',args=[8]))
        self.assertEqual(response.status_code,200)
        
    def test_AccountUpdateView_PATCH_fail(self):
        # id does not exist
        data = {
                    "email": "OrganizerTest@gmail.com",
                    "username": "OrganizerTest",
                    "password": "Test@Abcd",
                    "fname": "att3",
                    "lname": "dee3",
                    "gender": "Female",
                    "role": "ORGANIZER",
                }
        response = self.client.patch(reverse('RUD_account',args=[70]),data=data)
        self.assertEquals(response.status_code, 404)
        pass
    
    def test_AccountUpdateView_PATCH_pass(self):
        data = {
                    "email": "OrganizerTest@gmail.com",
                    "username": "OrganizerTest",
                    "password": "Test@Abcd",
                    "fname": "att3",
                    "lname": "dee3",
                    "gender": "Female",
                    "role": "ORGANIZER",
                }
        response = self.client.patch(reverse('RUD_account',args=[10]),data=data,content_type='application/json')
        self.assertEquals(response.status_code, 200)
        pass
    
    
    def test_LoginView_fail(self):
        # invalid credentials
        data = {
            "username": "OrganizerTest23",
            "password": "Test@Abcd",
        }
        response = self.client.post(reverse("user_login"),data=data,content_type='application/json')
        self.assertEqual(response.status_code,401)
    
    def test_LoginView_pass(self):
        data = {
            "username": "attendeeTest",
            "password": "Test@Abcd",
        }
        response = self.client.post(reverse("user_login"),data=data,content_type='application/json')
        self.assertEqual(response.status_code,200)
        pass
    
    def test_LogoutView_fail(self):
        # unauthorized
        response = self.client.post(reverse("user_logout"))
        self.assertEqual(response.status_code,401)
        pass
    
    def test_LogoutView_pass(self):
        data = {
            "username": "attendeeTest",
            "password": "Test@Abcd",
        }
        #login the user 
        response = self.client.post(reverse("user_login"),data=data,content_type='application/json')
        # save the token
        token = response.json()['token']
        headers = {"Authorization" : f"Token {token}"}
        
        #test logout
        response = Client(headers=headers).post(reverse("user_logout"))
        self.assertEqual(response.status_code,200)
        
        pass
    
    def test_AccountDeleteView_DELETE_fail(self):
        # user with id does not exist
        response = self.client.delete(reverse('RUD_account',args=[70]))
        self.assertEqual(response.status_code,404)
        pass
    
    def test_AccountDeleteView_DELETE_pass(self):
        response = self.client.delete(reverse('RUD_account',args=[5]))
        self.assertEqual(response.status_code,204)
        pass