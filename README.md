# Decor booking website (Django)

## Run it
```
python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations bookings
python manage.py migrate
python manage.py seed_site          # loads your 17 past-work photos + starter packages
python manage.py createsuperuser
python manage.py runserver
```
Site: http://127.0.0.1:8000  ·  Admin: http://127.0.0.1:8000/admin

## Change your details
Open `config/settings.py` and edit BRAND_NAME, WHATSAPP_NUMBER (country code + number, digits only),
PHONE_DISPLAY and INSTAGRAM_URL.

## Day to day (in /admin)
- **Bookings**: every request lands here. Change status to Confirmed / Completed / Cancelled.
- **Gallery items**: upload new photos, rename, reorder, or untick "Show on site" to hide one.
- **Packages**: edit names, what's included, and starting prices (the seeded prices are placeholders).

## Going live
Set environment variables DJANGO_DEBUG=0, DJANGO_SECRET_KEY, DJANGO_ALLOWED_HOSTS (and DJANGO_CSRF_ORIGINS
with your https domain), run `python manage.py collectstatic`, and serve /static and /media with your web
server (or add WhiteNoise for static files). Use a persistent disk for `media/` and `db.sqlite3`.
