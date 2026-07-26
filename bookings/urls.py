from django.urls import path
from . import views

urlpatterns = [
    # Home Page (Displays the movie list)
    path('', views.movie_list, name='home'),

    # Movie Details Page
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),

    # User Bookings Dashboard Page
    path('my-bookings/', views.my_bookings, name='my_bookings'),

    # Seat Booking Page
    path('book/<int:show_id>/', views.book_seat, name='book_seat'),

    # Cancel Ticket Page
    path('cancel-ticket/<int:booking_id>/', views.cancel_ticket, name='cancel_ticket'),

    # User Sign-Up Page
    path('signup/', views.signup, name='signup'),
]