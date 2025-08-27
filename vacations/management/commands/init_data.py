from django.core.management.base import BaseCommand
from datetime import date
from vacations.models import Role, User, Country, Vacation



class Command(BaseCommand):
    """
    Custom Django management command to populate the database with initial data.
    """

    help = "Populate the database with initial required data."

    def handle(self, *args, **kwargs) -> None:
        """
        Clears existing data and populates roles, users, countries, and vacations.
        Ensures clean state and consistent IDs.
        """

        # Step 1: Clear old data (important for consistent IDs)
        Vacation.objects.all().delete()
        Country.objects.all().delete()
        User.objects.all().delete()
        Role.objects.all().delete()

        # Step 2: Create roles
        admin_role = Role.objects.create(name="admin")
        user_role = Role.objects.create(name="user")

        # Step 3: Create users
        User.objects.create(
            email="admin@example.com",
            first_name="Admin",
            last_name="Manager",
            password="adminpass",
            role=admin_role,
            is_staff=True
        )

        User.objects.create(
            email="Dan@example.com",
            first_name="Dan",
            last_name="Doe",
            password="Danpass",
            role=user_role
        )

        # Step 4: Create countries
        country_names: list[str] = [
            "Israel", "USA", "France", "Germany",
            "Italy", "Spain", "Canada", "Brazil", "Japan", "Mexico"
        ]
        country_objs = [
            Country.objects.create(name=name) for name in country_names
        ]

        # Step 5: Create vacations (fixed order = fixed IDs)
        vacations_data: list[tuple[str, int, date, date, int, str]] = [
            ("Beach in Tel Aviv", 0, date(2025, 7, 10), date(2025, 7, 20), 2500, "tel_aviv.jpg"),
            ("New York City Trip", 1, date(2025, 8, 1), date(2025, 8, 10), 3500, "nyc.jpg"),
            ("Paris Adventure", 2, date(2025, 9, 5), date(2025, 9, 15), 3000, "paris.jpg"),
            ("Berlin History Tour", 3, date(2025, 10, 10), date(2025, 10, 20), 2700, "berlin.jpg"),
            ("Rome Exploration", 4, date(2025, 11, 1), date(2025, 11, 10), 3200, "rome.jpg"),
            ("Barcelona Highlights", 5, date(2025, 12, 15), date(2025, 12, 25), 2800, "barcelona.jpg"),
            ("Canadian Rockies", 6, date(2026, 1, 10), date(2026, 1, 20), 4000, "rockies.jpg"),
            ("Brazil Carnival", 7, date(2026, 2, 15), date(2026, 2, 25), 4500, "brazil.jpg"),
            ("Tokyo Cherry Blossoms", 8, date(2026, 3, 20), date(2026, 3, 30), 5000, "tokyo.jpg"),
            ("Mexico City Culture", 9, date(2026, 4, 5), date(2026, 4, 15), 3300, "mexico.jpg"),
            ("Dead Sea Relaxation", 0, date(2026, 5, 1), date(2026, 5, 10), 2200, "deadsea.jpg"),
            ("Miami Beach", 1, date(2026, 6, 10), date(2026, 6, 20), 3600, "miami.jpg"),
        ]

        for desc, country_idx, start, end, price, img in vacations_data:
            Vacation.objects.create(
                description=desc,
                country=country_objs[country_idx],
                start_date=start,
                end_date=end,
                price=price,
                image_filename=img
            )

        self.stdout.write(self.style.SUCCESS("✅ Database initialized successfully."))
