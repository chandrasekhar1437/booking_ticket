from django.core.management.base import BaseCommand
from bookings.models import Show, Seat  # Ensure model names match yours

class Command(BaseCommand):
    help = 'Automatically generates 50 seats for all shows'

    def handle(self, *args, **kwargs):
        rows = ['A', 'B', 'C', 'D', 'E']
        seats_per_row = 10
        shows = Show.objects.all()

        if not shows.exists():
            self.stdout.write(self.style.WARNING("No shows found. Please add a show in admin panel first."))
            return

        total_created = 0
        for show in shows:
            seats_to_create = []
            for row in rows:
                for num in range(1, seats_per_row + 1):
                    seat_num = f"{row}{num}"
                    
                    # Avoid duplicate seat creation
                    if not Seat.objects.filter(show=show, seat_number=seat_num).exists():
                        seats_to_create.append(Seat(show=show, seat_number=seat_num))
            
            if seats_to_create:
                Seat.objects.bulk_create(seats_to_create)
                total_created += len(seats_to_create)

        self.stdout.write(self.style.SUCCESS(f"Successfully generated {total_created} seats across {shows.count()} shows!"))