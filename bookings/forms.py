import re
from datetime import timedelta

from django import forms
from django.utils import timezone

from .models import Booking, Package


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["package", "celebrant", "event_date", "ready_by", "name", "phone", "email", "venue", "theme_notes"]
        widgets = {
            "event_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "venue": forms.Textarea(attrs={"rows": 2}),
            "theme_notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        f = self.fields
        f["package"].queryset = Package.objects.filter(is_active=True)
        f["package"].empty_label = "Not sure yet, suggest something"
        f["package"].label = "Setup"
        f["ready_by"].label = "Setup should be ready"
        f["event_date"].label = "Party date"
        f["event_date"].widget.attrs["min"] = (timezone.localdate() + timedelta(days=1)).isoformat()
        f["phone"].widget.attrs.update(placeholder="98765 43210", inputmode="tel", autocomplete="tel")
        f["name"].widget.attrs["autocomplete"] = "name"
        f["celebrant"].widget.attrs["placeholder"] = "e.g. Aarohi"
        f["venue"].widget.attrs["placeholder"] = "Flat / hall name, area, landmark"
        f["theme_notes"].widget.attrs["placeholder"] = "e.g. turning 2, pink and gold, butterfly theme, name on the neon sign"

    def clean_event_date(self):
        d = self.cleaned_data["event_date"]
        if d < timezone.localdate() + timedelta(days=1):
            raise forms.ValidationError("Pick a date from tomorrow onward. For same-day setups, message us on WhatsApp.")
        return d

    def clean_phone(self):
        digits = re.sub(r"[\s\-()]", "", self.cleaned_data["phone"])
        if not re.fullmatch(r"(\+?91)?[6-9]\d{9}", digits):
            raise forms.ValidationError("Enter a 10-digit Indian mobile number.")
        return digits[-10:]
