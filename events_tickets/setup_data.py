from accounts.models import Account
import json , random
from django.urls import reverse
from django.test import Client

def get_setup_data():
    client = Client()
    random_id = random.randint(1000,9999)
    attendee_user = Account.objects.create_user(email="attendeeTest1@gmail.com",
                    username = "attendeeTest",
                    password= "Test@Abcd",
                    fname= "att3",
                    lname= "dee3",
                    gender= "Female",
                    role= "ATTENDEE")
    attendee_id = attendee_user.id
        
    organizer_user = Account.objects.create_user(email="organizerTest@gmail.com",
                    username = "organizerTest",
                    password= "Test@Abcd",
                    fname= "org3",
                    lname= "zer3",
                    gender= "Female",
                    role= "ORGANIZER")
    organizer_id = organizer_user.id
        
    admin_user =  Account.objects.create_user(email="adminTest@gmail.com",
                    username = "adminTest",
                    password= "admin",
                    fname= "admin",
                    lname= "admin",
                    gender= "Male",
                    role= "ADMIN")
    admin_id = admin_user.id
    
    admin_data =json.dumps({'username' :  'adminTest', 'password' : 'admin'})
    attendee_data =json.dumps({'username' :  'attendeeTest', 'password' : 'Test@Abcd'})
    organizer_data =json.dumps({'username' :  'organizerTest', 'password' : 'Test@Abcd'})
        
    response = Client().post(path=reverse("user_login"),data=admin_data,content_type='application/json')
    admin_token = response.json()['token']
    
    response = Client().post(path=reverse("user_login"),data=attendee_data,content_type='application/json')
    attendee_token = response.json()['token']
    
    response = Client().post(path=reverse("user_login"),data=organizer_data,content_type='application/json')
    organizer_token = response.json()['token']
    
    data = {
        "client" : client,
        "random_id" : random_id,
        "attendee_user" : attendee_user,
        "attendee_id" : attendee_id,
        "attendee_token" : attendee_token,
        "attender_data" : attendee_data,
        "admin_user" : admin_user,
        "admin_id" : admin_id,
        "admin_token" : admin_token,
        "admin_data" : admin_data,
        "organizer_user" : organizer_user,
        "organizer_id" : organizer_id,
        "organizer_token" : organizer_token,
        "organizer_data" : organizer_data,
    }
    
    return data