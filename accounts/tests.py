from django.test import TestCase , Client
from django.urls import reverse
from accounts.models import Account
from accounts.serializers import AccountSerializer

class TestAccountViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.attendee_user = Account.objects.create(email="attendeeTest1@gmail.com",
                    username = "attendeeTest",
                    password= "Test@Abcd",
                    fname= "att3",
                    lname= "dee3",
                    gender= "Female",
                    role= "ATTENDEE")
        
        self.organizer_user = Account.objects.create(email="organizerTest@gmail.com",
                    username = "organizerTest",
                    password= "Test@Abcd",
                    fname= "org3",
                    lname= "zer3",
                    gender= "Female",
                    role= "ORGANIZER")
        
        self.admin_user =  Account.objects.create(email="adminTest@gmail.com",
                    username = "adminTest",
                    password= "admin",
                    fname= "admin",
                    lname= "admin",
                    gender= "Male",
                    role= "ADMIN")
        response = self.client.post(reverse("user_login"),data=AccountSerializer(self.admin_user).data,content_type='application/json')
        self.admin_token = response.json()['token']
        
        response = self.client.post(reverse("user_login"),data=AccountSerializer(self.attendee_user).data,content_type='application/json')
        self.attendee_token = response.json()['token']
        
        response = self.client.post(reverse("user_login"),data=AccountSerializer(self.organizer_user).data,content_type='application/json')
        self.organizer_token = response.json()['token']
        


    
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
                    "username": "OrganizerTest1",
                    "password": "Test@Abcd",
                    "fname": "org4",
                    "lname": "zer4",
                    "gender": "Female",
                    "role": "ORGANIZER",
                }
        response = self.client.post(reverse('LC_account'),data)
        self.assertEquals(response.status_code, 201)
        
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
        
    
    def test_LogoutView_fail(self):
        # unauthorized
        response = self.client.post(reverse("user_logout"))
        self.assertEqual(response.status_code,401)
    
        
    def test_AccountListView_GET_fail_unauthenticated(self):
        # list all account fail - unauthenticated user not allowed
        response = self.client.get(reverse('LC_account'))
        self.assertEquals(response.status_code, 401)
        
       
    def test_AccountListView_GET_fail_org(self):
        # list all account fail organizer user 
        response = self.client.get(reverse('LC_account'),HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEquals(response.status_code, 403)
    
    def test_AccountListView_GET_fail_att(self):
        # list all account fail attendee user  
        response = self.client.get(reverse('LC_account'),HTTP_AUTHORIZATION=f'Token {self.attendee_token}')
        self.assertEquals(response.status_code, 403)
        
    def test_AccountListView_GET_pass_admin(self):
        # list all account success - only admin can get all the users 
        response = self.client.get(reverse('LC_account'),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        self.assertEquals(response.status_code, 200)
        
    def test_AccountRetrieveView_Get_fail(self):
        # id not found
        response = self.client.get(reverse('RUD_account',args=[70]),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        self.assertEqual(response.status_code,404)
        
    
    def test_AccountRetrieveView_Get_pass_admin(self):
        # id found
        # admin can view any account
        # response = self.client.get(reverse('LC_account'),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        # print(response.json())
        response = self.client.get(reverse('RUD_account',args=[29]),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        self.assertEqual(response.status_code,200)
        
    def test_AccountRetrieveView_Get_fail_org(self):
        # id found
        # organizer cant see any other account
        response = self.client.get(reverse('RUD_account',args=[29]),HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEqual(response.status_code,403)
        
    def test_AccountRetrieveView_Get_pass_org(self):
        # id found
        # organizer cant see self account
        # response = self.client.get(reverse('LC_account'),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        # print(response.json())
        response = self.client.get(reverse('RUD_account',args=[36]),HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEqual(response.status_code,200)
        
    def test_AccountRetrieveView_Get_fail_att(self):
        # id found
        # attendee cant see any other account
        response = self.client.get(reverse('RUD_account',args=[30]),HTTP_AUTHORIZATION=f'Token {self.attendee_token}')
        self.assertEqual(response.status_code,403)
        
    def test_AccountRetrieveView_Get_pass_att(self):
        # id found
        # attendee can see self account
        # response = self.client.get(reverse('LC_account'),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        # print(response.json())
        response = self.client.get(reverse('RUD_account',args=[32]),HTTP_AUTHORIZATION=f'Token {self.attendee_token}')
        self.assertEqual(response.status_code,200)
        
    
    def test_AccountUpdateView_PATCH_fail_att(self):
        # only self and admin can update
        # response = self.client.get(reverse('LC_account'),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        # print(response.json())
        data = {
                    "email": "OrganizerTest@gmail.com",
                    "username": "OrganizerTest",
                    "password": "Test@Abcd",
                    "fname": "att3",
                    "lname": "dee3",
                    "gender": "Female",
                    "role": "ORGANIZER",
                }
        response = self.client.patch(reverse('RUD_account',args=[39]),data=data,HTTP_AUTHORIZATION=f'Token {self.attendee_token}')
        self.assertEquals(response.status_code, 403)
        
    def test_AccountUpdateView_PATCH_pass_org(self):
        # only self and admin can update
        # response = self.client.get(reverse('LC_account'),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        # print(response.json())
        data = {
                    "email": "OrganizerTest@gmail.com",
                    "username": "OrganizerTest",
                    "password": "Test@Abcd",
                    "fname": "org4",
                    "lname": "org4",
                    "gender": "Female",
                    "role": "ORGANIZER",
                }
        response = self.client.patch(reverse('RUD_account',args=[45]),data=data,HTTP_AUTHORIZATION=f'Token {self.organizer_token}',content_type='application/json')
        self.assertEquals(response.status_code, 200)
        
    def test_AccountUpdateView_PATCH_pass_admin(self):
        # only self and admin can update
        # response = self.client.get(reverse('LC_account'),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        # print(response.json())
        data = {
                    "email": "OrganizerTest1@gmail.com",
                    "username": "OrganizerTest",
                    "password": "Test@Abcd",
                    "fname": "org4",
                    "lname": "org4",
                    "gender": "Male",
                    "role": "ORGANIZER",
                }
        
        response = self.client.patch(reverse('RUD_account',args=[42]),data=data,HTTP_AUTHORIZATION=f'Token {self.admin_token}',content_type='application/json')
        self.assertEquals(response.status_code, 200)
        # response = self.client.get(reverse('LC_account'),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        # print(response.json())
    

class TestAccountDeleteLogoutViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.attendee_user = Account.objects.create(email="attendeeTest1@gmail.com",
                    username = "attendeeTest",
                    password= "Test@Abcd",
                    fname= "att3",
                    lname= "dee3",
                    gender= "Female",
                    role= "ATTENDEE")
        
        self.organizer_user = Account.objects.create(email="organizerTest@gmail.com",
                    username = "organizerTest",
                    password= "Test@Abcd",
                    fname= "org3",
                    lname= "zer3",
                    gender= "Female",
                    role= "ORGANIZER")
        
        self.admin_user =  Account.objects.create(email="adminTest@gmail.com",
                    username = "adminTest",
                    password= "admin",
                    fname= "admin",
                    lname= "admin",
                    gender= "Male",
                    role= "ADMIN")
        response = self.client.post(reverse("user_login"),data=AccountSerializer(self.admin_user).data,content_type='application/json')
        self.admin_token = response.json()['token']
        
        response = self.client.post(reverse("user_login"),data=AccountSerializer(self.attendee_user).data,content_type='application/json')
        self.attendee_token = response.json()['token']
        
        response = self.client.post(reverse("user_login"),data=AccountSerializer(self.organizer_user).data,content_type='application/json')
        self.organizer_token = response.json()['token']

    def test_AccountDeleteView_DELETE_fail(self):
        # user with id does not exist
        # response = self.client.get(reverse('LC_account'),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        # print(response.json())
        response = self.client.delete(reverse('RUD_account',args=[70]),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        self.assertEqual(response.status_code,404)
        
    
    def test_AccountDeleteView_DELETE_fail_att(self):
        # attendee should not be able to delete any account other than self
        # must be logged in
        response = self.client.delete(reverse('RUD_account',args=[5]))
        self.assertEqual(response.status_code,401)
        
    def test_AccountDeleteView_DELETE_fail_att_other(self):
        # attendee should not be able to delete any account other than self
        # must be logged in
        response = self.client.delete(reverse('RUD_account',args=[5]),HTTP_AUTHORIZATION=f'Token {self.attendee_token}')
        self.assertEqual(response.status_code,403)
        
    def test_AccountDeleteView_DELETE_pass_att_self(self):
        # attendee should not be able to delete any account other than self
        # must be logged in
        # response = self.client.get(reverse('LC_account'),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        # print(response.json())
        response = self.client.delete(reverse('RUD_account',args=[10]),HTTP_AUTHORIZATION=f'Token {self.attendee_token}')
        self.assertEqual(response.status_code,204)
        # response = self.client.get(reverse('LC_account'),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        # print(response.json())
        
        
    def test_AccountDeleteView_DELETE_pass_org_admin(self):
        # admin should be able to delete any account 
        # must be logged in
        # response = self.client.get(reverse('LC_account'),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        # print(response.json())
        response = self.client.delete(reverse('RUD_account',args=[13]),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        self.assertEqual(response.status_code,204)
        # response = self.client.get(reverse('LC_account'),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        # print(response.json())
    
        
    def test_LogoutView_pass(self):
        response = self.client.post(reverse("user_logout"),HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEqual(response.status_code,200)
        