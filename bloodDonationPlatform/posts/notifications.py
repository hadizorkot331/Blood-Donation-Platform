import smtplib
from django.urls import reverse
from django.core.mail import send_mass_mail
from users.models import Profile
from django.conf import settings
from .whatsappGroup import getinvitelink
import requests


def send_whatsapp_message(
    needed_blood_type,
    hospital,
    compatible_blood_types,
    description,
    post_id,
    grp_id="120363317413351438@g.us",
):
    url = "https://gate.whapi.cloud/messages/text"
    invite_link = getinvitelink()
    message = f"URGENT BLOOD DONATION NEEDED\n\n\nThe patient's blood type is {needed_blood_type} and is compatible with {', '.join(compatible_blood_types)}.\n\nThe blood is needed at {hospital}.\n\nThe description of this post is: {description}.\n\n\nPlease follow this link to view this post on the website: {settings.HOST + reverse('posts:detailed-post', kwargs={'post_id':post_id})}\n\n\n   --------------------   {invite_link}"

    payload = {"to": grp_id, "body": message, "typing_time": 0}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {settings.WHATSAPP_API_KEY}",
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        return True
    except (requests.HTTPError, ConnectionError, TimeoutError):
        return False


def notify_compatible_users(
    needed_blood_type, hospital, compatible_blood_types, caza, description, post_id
):
    compatible_users = (
        Profile.objects.filter(notifications=True)
        .filter(blood_type__in=compatible_blood_types)
        .filter(caza=caza)
        .values_list(("email"))
    )
    compatible_user_emails = [value[0] for value in compatible_users]

    message_text = f"You are being contacted because you are eligible to donate to this urgent blood request.\n\n\nThe patient's blood type is {needed_blood_type} and is compatible with {', '.join(compatible_blood_types)}.\n\nThe blood is needed at {hospital}.\n\nThe description of this post is: {description},\n\n\nPlease follow this link to view this post on the website: {settings.HOST + reverse('posts:detailed-post', kwargs={'post_id':post_id})}"

    message_title = f"{needed_blood_type} Blood Urgently Needed At {hospital}"
    message_list = [
        (
            str(message_title),
            str(message_text),
            str(settings.EMAIL_HOST_USER),
            [str(user_email)],
        )
        for user_email in compatible_user_emails
    ]
    try:
        send_mass_mail(message_list, fail_silently=False)
        return True
    except smtplib.SMTPException:
        return False
