from django.core.management.base import BaseCommand

from bookings.models import GalleryItem as G, Package

WORK = [
    ("Barbie-theme 1st birthday stage", G.KIDS),
    ("Powerpuff Girls ring in rose gold", G.RING),
    ("2nd birthday ring in pink, purple and gold", G.RING),
    ("Rose-gold ring for a 30th birthday", G.RING),
    ("Butterfly and crown ring in pink and gold", G.RING),
    ("Welcome baby boy backdrop", G.BABY),
    ("Name-letter pillars with butterfly arch", G.KIDS),
    ("Unicorn birthday stage", G.KIDS),
    ("Black and gold entrance arch", G.ARCH),
    ("Purple butterfly ring", G.RING),
    ("Pastel ring for a 1st birthday", G.RING),
    ("Gold and ivory ring for an evening party", G.RING),
    ("Violet chrome ring", G.RING),
    ("Welcome baby at home", G.BABY),
    ("Silver, black and white ring", G.RING),
    ("Orange and gold terrace ring", G.RING),
    ("Butterfly garden ring in purple and gold", G.RING),
]

# Starting prices are placeholders: change them in the admin.
PACKAGES = [
    ("ring-arch", "Ring arch setup", "A balloon ring with a neon sign", 4999,
     "Balloon ring arch in your colours\nNeon 'Happy Birthday' sign\nNumber or letter foil balloons"),
    ("name-age", "Name and age setup", "Ring or arch with the birthday star's name", 6999,
     "Ring or arch backdrop\nName letters and age number\nBalloon pillars for the cake table"),
    ("theme-stage", "Kids theme stage", "Full backdrop for character themes", 11999,
     "Printed or cut-out character backdrop\nFoil curtain and arches on both sides\nTable and prop styling"),
    ("milestone", "Milestone birthday arch", "Chrome balloons for 18th, 30th, 50th", 5999,
     "Chrome balloon arch or ring\nGold foil number balloons\nCeiling balloons with ribbons"),
    ("welcome-baby", "Welcome baby at home", "For bringing the baby home", 3499,
     "Foil curtain and message balloons\nBalloon pillars\nBalloons on the ceiling"),
]


class Command(BaseCommand):
    help = "Loads the past-work photos and starter packages. Safe to run more than once."

    def handle(self, *args, **options):
        for i, (title, cat) in enumerate(WORK, 1):
            GalleryItem = G.objects.get_or_create(
                image=f"gallery/work-{i:02d}.jpg",
                defaults={"title": title, "category": cat, "order": i},
            )
        for i, (slug, name, tag, price, inc) in enumerate(PACKAGES, 1):
            Package.objects.get_or_create(
                slug=slug,
                defaults={"name": name, "tagline": tag, "price_from": price, "includes": inc, "order": i},
            )
        self.stdout.write(self.style.SUCCESS("Past work and packages loaded."))
