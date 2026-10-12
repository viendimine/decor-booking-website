from django.conf import settings


def site(request):
    return {
        "BRAND": settings.BRAND_NAME,
        "WHATSAPP": settings.WHATSAPP_NUMBER,
        "PHONE_DISPLAY": settings.PHONE_DISPLAY,
        "INSTAGRAM": settings.INSTAGRAM_URL,
    }
