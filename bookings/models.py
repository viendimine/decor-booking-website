from django.db import models
from django.utils.crypto import get_random_string


class Package(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=160)
    includes = models.TextField(help_text="One item per line.")
    price_from = models.PositiveIntegerField(help_text="Starting price in rupees.")
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True, verbose_name="Show on site")

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    @property
    def includes_list(self):
        return [line.strip() for line in self.includes.splitlines() if line.strip()]


class GalleryItem(models.Model):
    RING, KIDS, BABY, ARCH = "ring", "kids", "baby", "arch"
    CATEGORIES = [
        (RING, "Ring arches"),
        (KIDS, "Kids themes"),
        (BABY, "Welcome baby"),
        (ARCH, "Arches & stages"),
    ]
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORIES, default=RING)
    image = models.ImageField(upload_to="gallery/")
    order = models.PositiveSmallIntegerField(default=0)
    is_visible = models.BooleanField(default=True, verbose_name="Show on site")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created"]

    def __str__(self):
        return self.title


class Booking(models.Model):
    NEW, CONFIRMED, DONE, CANCELLED = "new", "confirmed", "done", "cancelled"
    STATUSES = [(NEW, "New"), (CONFIRMED, "Confirmed"), (DONE, "Completed"), (CANCELLED, "Cancelled")]
    READY_BY = [
        ("12:00", "By 12 pm"),
        ("16:00", "By 4 pm"),
        ("19:00", "By 7 pm"),
        ("21:00", "By 9 pm"),
    ]

    reference = models.CharField(max_length=12, unique=True, editable=False)
    status = models.CharField(max_length=10, choices=STATUSES, default=NEW)
    package = models.ForeignKey(Package, null=True, blank=True, on_delete=models.SET_NULL)
    celebrant = models.CharField("Birthday person's name", max_length=60)
    event_date = models.DateField()
    ready_by = models.CharField(max_length=5, choices=READY_BY, default="16:00")
    name = models.CharField("Your name", max_length=80)
    phone = models.CharField("WhatsApp / phone number", max_length=15)
    email = models.EmailField(blank=True)
    venue = models.TextField("Venue address")
    theme_notes = models.TextField("Theme, colours, age or anything else", blank=True)
    internal_notes = models.TextField(blank=True, help_text="Only visible in admin.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["event_date", "created_at"]

    def __str__(self):
        return f"{self.reference} · {self.celebrant} · {self.event_date:%d %b %Y}"

    def save(self, *args, **kwargs):
        if not self.reference:
            while True:
                ref = "BB" + get_random_string(6, "ABCDEFGHJKLMNPQRSTUVWXYZ23456789")
                if not Booking.objects.filter(reference=ref).exists():
                    self.reference = ref
                    break
        super().save(*args, **kwargs)
