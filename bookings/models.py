from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    language = models.CharField(max_length=50)
    release_date = models.DateField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)

    def __str__(self):
        return self.title


class Theater(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.city}"


class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='shows')
    show_time = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=150.00)

    def __str__(self):
        return f"{self.movie.title} | {self.theater.name} | {self.show_time.strftime('%Y-%m-%d %H:%M')}"


class Seat(models.Model):
    seat_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.seat_number


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='bookings')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('show', 'seat')  # ఒకే సీటును ఒకే షోకి ఇద్దరు బుక్ చేయకుండా నిరోధిస్తుంది

    def __str__(self):
        return f"{self.user.username} - {self.show.movie.title} - Seat: {self.seat.seat_number}"