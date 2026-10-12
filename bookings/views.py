from urllib.parse import quote

from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm
from .models import Booking, GalleryItem, Package


def home(request):
    return render(request, "index.html", {
        "packages": Package.objects.filter(is_active=True),
        "work": GalleryItem.objects.filter(is_visible=True)[:8],
    })


def gallery(request):
    return render(request, "gallery.html", {
        "items": GalleryItem.objects.filter(is_visible=True),
        "categories": GalleryItem.CATEGORIES,
    })


def book(request):
    initial = {}
    slug = request.GET.get("package")
    if slug:
        pkg = Package.objects.filter(slug=slug, is_active=True).first()
        if pkg:
            initial["package"] = pkg
    form = BookingForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        booking = form.save()
        return redirect("booked", reference=booking.reference)
    return render(request, "book.html", {"form": form})


def booked(request, reference):
    b = get_object_or_404(Booking, reference=reference)
    msg = (
        f"Hi! I just requested a booking ({b.reference}) for {b.celebrant}'s birthday on "
        f"{b.event_date:%d %b %Y}. Please confirm availability."
    )
    wa_url = f"https://wa.me/{settings.WHATSAPP_NUMBER}?text={quote(msg)}"
    return render(request, "booked.html", {"b": b, "wa_url": wa_url})
