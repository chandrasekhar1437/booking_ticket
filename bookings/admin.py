from django.contrib import admin
from .models import Movie, Theater, Show, Seat, Booking

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'duration', 'release_date')
    search_fields = ('title', 'language')

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ('name', 'city')

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('movie', 'theater', 'show_time', 'price')
    list_filter = ('theater', 'show_time')

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number',)
    search_fields = ('seat_number',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'show', 'seat', 'booked_at')
    list_filter = ('booked_at', 'show')