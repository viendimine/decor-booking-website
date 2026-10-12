from django.contrib import admin
from django.utils.html import format_html

from .models import Booking, GalleryItem, Package


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["reference", "celebrant", "event_date", "ready_by", "package", "name", "phone", "status"]
    list_editable = ["status"]
    list_filter = ["status", "event_date", "package"]
    search_fields = ["reference", "celebrant", "name", "phone", "venue"]
    date_hierarchy = "event_date"
    readonly_fields = ["reference", "created_at"]
    actions = ["mark_confirmed"]

    @admin.action(description="Mark selected as confirmed")
    def mark_confirmed(self, request, queryset):
        queryset.update(status=Booking.CONFIRMED)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ["name", "price_from", "order", "is_active"]
    list_editable = ["price_from", "order", "is_active"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ["thumb", "title", "category", "order", "is_visible"]
    list_editable = ["title", "category", "order", "is_visible"]
    list_filter = ["category", "is_visible"]

    @admin.display(description="Photo")
    def thumb(self, obj):
        return format_html('<img src="{}" style="height:56px;border-radius:6px">', obj.image.url)
