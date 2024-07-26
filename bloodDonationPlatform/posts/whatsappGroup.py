import requests
from django.conf import settings


def getinvitelink(grp_id="120363317413351438%40g.us"):
    url = f"https://gate.whapi.cloud/groups/{grp_id}/invite"

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {settings.WHATSAPP_API_KEY}",
    }

    response = requests.get(url, headers=headers).json()

    code = response["invite_code"]

    return f"https://chat.whatsapp.com/{code}"
