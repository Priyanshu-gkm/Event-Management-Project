from django.core.mail import send_mail
from events_tickets.models import Ticket, Event
from accounts.models import Account
from datetime import datetime, timedelta
from Event_Management.settings import EMAIL_HOST_USER


def send_mail_to_attendees():
    tickets = (
        Ticket.objects.filter(event__date__lte=datetime.now().date() + timedelta(1))
        .values_list("event_id", "customer_id")
        .distinct()
    )
    # "(event_id,customer_id)"
    for i in tickets:
        event = Event.objects.get(id=i[0])
        attendee = Account.objects.get(id=i[1])
        subject = f"Reminder for {event.name} Event"
        message = f"""
        Hello {attendee.fname +" "+ attendee.lname}
        This is to remind you that you have booked a ticket for event {event.name}. The details are as follows :
        
        Event name : {event.name}
        Event Date : {event.date}
        Event time : {event.time}
        Event location : {event.location}
        
        This is a reminder email for the event mentioned above. Hope to see you on time. Have a great event.
        Thank you.
        """
        # print(attendee.email)
        send_mail(
            subject,
            message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[attendee.email],
        )
