from urllib.parse import quote
from pathlib import Path

from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm
from .models import Booking, GalleryItem, Package


def get_gallery_images():
    """Load gallery images directly from media/gallery/."""
    gallery_dir = Path(settings.MEDIA_ROOT) / "gallery"

    if not gallery_dir.exists():
        return []

    images = []

    for image_path in sorted(gallery_dir.glob("work-*")):
        if image_path.suffix.lower() not in {
            ".jpg", ".jpeg", ".png", ".webp"
        }:
            continue

        images.append({
            "title": image_path.stem.replace("-", " ").title(),
            "image": {
                "url": f"{settings.MEDIA_URL}gallery/{image_path.name}"
            },
            "category": "ring",
        })

    return images


def home(request):
    return render(request, "index.html", {
        "packages": Package.objects.filter(is_active=True),
        "work": get_gallery_images()[:8],
    })


def gallery(request):
    return render(request, "gallery.html", {
        "items": get_gallery_images(),
        "categories": GalleryItem.CATEGORIES,
    })


def book(request):
    initial = {}
    slug = request.GET.get("package")

    if slug:
        pkg = Package.objects.filter(
            slug=slug, is_active=True
        ).first()

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
        f"Hi! I just requested a booking ({b.reference}) for "
        f"{b.celebrant}'s birthday on {b.event_date:%d %b %Y}. "
        "Please confirm availability."
    )

    wa_url = (
        f"https://wa.me/{settings.WHATSAPP_NUMBER}?text={quote(msg)}"
    )

    return render(
        request,
        "booked.html",
        {"b": b, "wa_url": wa_url},
    )
