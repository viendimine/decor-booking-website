from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = f"{settings.BRAND_NAME} bookings"
admin.site.site_title = settings.BRAND_NAME

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("bookings.urls")),

    # Serve committed gallery images
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]
