from django.core.mail import send_mass_mail
from users.models import Profile
from django.conf import settings
import requests


def send_whatsapp_message(grp_id="120363317413351438@g.us", message=""):
    url = "https://gate.whapi.cloud/messages/text"

    payload = {"to": grp_id, "body": message, "typing_time": 0}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {settings.WHATSAPP_API_KEY}",
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


def notify_compatible_users(needed_blood_type, hospital, compatible_blood_types, caza):
    compatible_users = (
        Profile.objects.filter(blood_type__in=compatible_blood_types)
        .filter(caza=caza)
        .values_list(("email"))
    )
    compatible_user_emails = [value[0] for value in compatible_users]
    message_text = f"{needed_blood_type} blood urgently needed at {hospital}"
    message_list = [
        (
            str("URGENT BLOOD DONATION REQUEST"),
            str(message_text),
            str(settings.EMAIL_HOST_USER),
            [str(user_email)],
        )
        for user_email in compatible_user_emails
    ]
    send_mass_mail(message_list, fail_silently=False)
